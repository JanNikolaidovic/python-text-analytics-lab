#!/usr/bin/env python3
"""Build onboarding/video_recording_guide.pdf, the instructor guide for recording the onboarding videos.

The shot lists (sections 5 and 6) mirror video01_setup_and_first_lab.md and video02_loading_course_data.md:
when you change a script there, change it here too and rebuild.

Needs reportlab and the DejaVu fonts (for Greek text and symbols). reportlab isn't in the course .venv,
so use a throwaway environment:
    python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install reportlab
    /tmp/pdfenv/bin/python onboarding/build_recording_guide.py
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

OUT = Path(__file__).with_name("video_recording_guide.pdf")
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", FONT_DIR + "DejaVuSansMono.ttf"))
for bold, italic in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    addMapping("DV", bold, italic, "DV-B" if bold else "DV")

INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5f6b7a")
ACCENT = colors.HexColor("#2457c5")
ACCENT_BG = colors.HexColor("#eef3fc")
PANEL = colors.HexColor("#f4f5f7")
RULE = colors.HexColor("#d8dce3")
SAY_BG = colors.HexColor("#f1f8f3")
SAY_RULE = colors.HexColor("#3f9a5c")
WARN_BG = colors.HexColor("#fff6e5")
WARN_RULE = colors.HexColor("#d08a12")


def style(name, size, leading, font="DV", color=INK, **kw):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading, textColor=color,
                          alignment=kw.pop("alignment", TA_LEFT), bulletFontName="DV", **kw)


S = {
    "title": style("title", 24, 29, "DV-B", spaceAfter=4),
    "subtitle": style("subtitle", 11.5, 16, color=MUTED),
    "h1": style("h1", 16, 20, "DV-B", ACCENT, spaceBefore=4, spaceAfter=8),
    "h2": style("h2", 12, 16, "DV-B", spaceBefore=10, spaceAfter=5),
    "body": style("body", 9.6, 14, spaceAfter=5),
    "small": style("small", 8.6, 12),
    "cell": style("cell", 8.8, 12.2),
    "cellb": style("cellb", 8.8, 12.2, "DV-B"),
    "say": style("say", 8.9, 12.6, color=colors.HexColor("#1d4d2c"), spaceAfter=4),
    "bullet": style("bullet", 9.6, 14, leftIndent=14, bulletIndent=3, spaceAfter=2.5),
    "check": style("check", 9.4, 13.6, leftIndent=16, bulletIndent=1, spaceAfter=3),
    "head": style("head", 8.8, 12.2, color=colors.white),
    "headsmall": style("headsmall", 8.6, 12, color=colors.white, alignment=TA_RIGHT),
    "step": style("step", 8.8, 12.2, leftIndent=12, bulletIndent=0, spaceAfter=2.5),
}

W = A4[0] - 36 * mm  # usable width


def P(text, st="body"):
    return Paragraph(text, S[st])


def key(k):
    return f'<font name="DVM" size="8.4">{k}</font>'


WSL = key("\\\\wsl$")


def bullets(items, st="bullet", sym="•"):
    return [Paragraph(t, S[st], bulletText=sym) for t in items]


def checklist(items):
    return bullets(items, "check", "☐")


def box(flowables, bg=ACCENT_BG, rule=ACCENT, pad=8):
    t = Table([[flowables]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, rule),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + 2), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad), ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 2),
    ]))
    return t


def grid(rows, widths):
    data = [[P(c, "cellb" if r == 0 else "cell") for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=[W * w for w in widths], repeatRows=1)
    st = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_BG), ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT),
    ]
    st += [("BACKGROUND", (0, r), (-1, r), PANEL) for r in range(2, len(rows), 2)]
    t.setStyle(TableStyle(st))
    return t


def scene(num, title, timing, show, say, note=None):
    head = Table([[P(f"<b>Scene {num}</b>  ·  {title}", "head"), P(timing, "headsmall")]],
                 colWidths=[W * 0.8, W * 0.2])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    show_cell = [P("<b>ON SCREEN</b>", "small")] + [
        Paragraph(s, S["step"], bulletText=f"{i}.") for i, s in enumerate(show, 1)]
    say_cell = [P("<b>SAY</b>", "small")] + [P(s, "say") for s in say]
    body = Table([[show_cell, say_cell]], colWidths=[W * 0.46, W * 0.54])
    body.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), PANEL), ("BACKGROUND", (1, 0), (1, 0), SAY_BG),
        ("LINEBEFORE", (1, 0), (1, 0), 2, SAY_RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    parts = [head, body]
    if note:
        parts.append(box([P(note, "cell")], WARN_BG, WARN_RULE, pad=6))
    return KeepTogether(parts + [Spacer(1, 9)])


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.8)
    canvas.setFillColor(MUTED)
    if doc.page > 1:
        canvas.drawString(18 * mm, A4[1] - 11 * mm, "Recording the Colab onboarding videos")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, A4[1] - 12.8 * mm, A4[0] - 18 * mm, A4[1] - 12.8 * mm)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
    canvas.drawString(18 * mm, 10 * mm, "Python Text Analytics Lab · University of Piraeus")
    canvas.restoreState()


story = []

# ---------------------------------------------------------------- cover
story += [
    Spacer(1, 6),
    P("INSTRUCTOR GUIDE", "small"),
    Spacer(1, 3),
    P("Recording the Colab Onboarding Videos", "title"),
    P("How to prepare, record, edit and publish the two short videos that get students from the course zip "
      "to a running Colab notebook.", "subtitle"),
    Spacer(1, 14),
    P("The two videos", "h2"),
    grid([
        ["Video", "Students watch it", "Length", "What it shows"],
        ["<b>1 · Setting up and opening your first lab</b>", "Before Lab 01", "≈ 8 min",
         "Welcome and course overview, then: download and unzip the course, upload the folder to Google Drive, "
         "open Lab 01 in Colab, run cells, recover after a reset, how work is saved."],
        ["<b>2 · Loading the course data</b>", "Before Lab 08 (relink at Lab 12)", "≈ 4 min",
         "The Drive permission screens, where the data lives, what to do after a break, the “data folder not "
         "found” message."],
    ], [0.26, 0.17, 0.11, 0.46]),
    Spacer(1, 12),
    P("The whole process", "h2"),
    grid([
        ["Step", "What you do", "Time"],
        ["1", "<b>Choose a recording tool</b> and set it up (sections 1 and 2).", "15–30 min"],
        ["2", "<b>Prepare your PC, a test Google account and three welcome slides</b> (section 3).",
         "45 min, once"],
        ["3", "<b>Rehearse</b> each video once without recording, following the shot list.", "15 min"],
        ["4", "<b>Record scene by scene</b> (section 4, shot lists in sections 5 and 6).", "1–2 hours"],
        ["5", "<b>Edit</b>: trim, join, add a title card and captions (section 7).", "1 hour"],
        ["6", "<b>Export and publish</b>, then paste the links into the platform text (section 8).", "30 min"],
    ], [0.08, 0.75, 0.17]),
    Spacer(1, 12),
    box([
        P("<b>Files in the repo that go with this guide</b>", "cell"),
        Spacer(1, 3),
        P(f"{key('onboarding/video01_setup_and_first_lab.md')} and "
          f"{key('onboarding/video02_loading_course_data.md')}: the same scripts as sections 5 and 6, in "
          f"editable form.<br/>"
          f"{key('onboarding/platform_text.md')}: the student instructions for the university platform, with "
          f"two placeholders for the video links.<br/>"
          f"{key('make_student_zip.py')}: builds {key('dist/python_lab.zip')}, the file the videos show.<br/>"
          f"{key('onboarding/build_recording_guide.py')}: rebuilds this PDF.",
          "cell"),
    ]),
    PageBreak(),
]

# ---------------------------------------------------------------- 1-2. tools
story += [
    P("1. Choose your recording tool", "h1"),
    P("You need something that records your screen together with your microphone, and something to trim and join "
      "the clips. Everything below is free and runs on Windows. Video 1 shows File Explorer as well as the "
      "browser, so the tool must be able to record the <b>whole screen</b>, not only a browser tab."),
    Spacer(1, 4),
    grid([
        ["Tool", "How to start it", "Good for", "Watch out for"],
        ["<b>Clipchamp</b><br/>(built into Windows 11; free in the Microsoft Store for Windows 10)",
         "Start menu → Clipchamp → <b>Create a new video</b> → <b>Record &amp; create</b> → <b>Screen</b>",
         "Recording <i>and</i> editing in one app. Auto-captions. Free 1080p export. Can add your webcam.",
         "Pick <b>Entire screen</b> when it asks what to share. Each recording has a length cap (around 30 "
         "minutes), far more than one scene needs."],
        ["<b>OBS Studio</b><br/>(obsproject.com)",
         "Install, then accept the <b>Auto-Configuration Wizard</b> → “Optimize just for recording”",
         "Best quality and control. Records any screen content. Hotkeys to start, pause and stop.",
         "About 15 minutes of setup. No editing: pair it with Clipchamp."],
        ["<b>Snipping Tool</b><br/>(Windows 11)",
         f"{key('Win + Shift + R')}, drag over the area, then <b>Start</b>",
         "No setup at all. Good for a quick test take.",
         "No editing. Check the microphone icon in its toolbar is switched on."],
        ["<b>PowerPoint</b>",
         "<b>Insert → Screen Recording</b>",
         "If you already work in PowerPoint; the welcome slides live in the same file.",
         "To get the video out: right-click it → <b>Save Media As</b>. Less control than the others."],
        ["<b>Xbox Game Bar</b>", f"{key('Win + Alt + R')}", "Not recommended.",
         "Records a single app window only: it can't capture File Explorer or the desktop, which Video 1 needs."],
        ["<b>Loom</b> (free plan)", "Browser extension", "Not recommended.",
         "At the time of writing the free plan caps recordings at 5 minutes, shorter than Video 1."],
    ], [0.18, 0.25, 0.26, 0.31]),
    Spacer(1, 10),
    box([
        P("<b>Recommendation</b>", "cell"),
        Spacer(1, 3),
        P("<b>Option A, simplest:</b> Clipchamp for everything. Record each scene inside Clipchamp, the clips land "
          "on the timeline in order, and you edit and export in the same place. Choose this if it's your first "
          "screen recording.", "cell"),
        Spacer(1, 3),
        P("<b>Option B, best quality:</b> OBS Studio to record, Clipchamp to edit. Worth it if you plan to make "
          "more course videos later.", "cell"),
    ]),
    Spacer(1, 6),
    P("<i>On a Mac instead?</i> Press " + key("Cmd + Shift + 5") + " to record the screen (choose your microphone "
      "under <b>Options</b>) and edit in iMovie. Everything else in this guide applies unchanged.", "small"),
    Spacer(1, 6),
    P("2. Set up the tool you chose", "h1"),
    P("Option A · Clipchamp", "h2"),
    *bullets([
        "Open <b>Clipchamp</b> and sign in with your Microsoft account (personal or university).",
        "Click <b>Create a new video</b>. In the left menu choose <b>Record &amp; create</b> → <b>Screen</b> "
        "(or <b>Screen and camera</b> for the welcome scenes if you want your webcam in the corner).",
        "Allow microphone access when asked, and pick your microphone in the dropdown. Speak: the level bar "
        "should move.",
        "Click the red record button, choose <b>Entire screen</b>, then <b>Share</b>. Do the scene.",
        "Stop the recording and click <b>Save and edit</b>. The clip is added to the timeline. Repeat for the "
        "next scene.",
    ]),
    P("Option B · OBS Studio", "h2"),
    *bullets([
        "Install from <b>obsproject.com</b>, open it, and run the <b>Auto-Configuration Wizard</b> "
        "(Tools menu) → <b>Optimize just for recording</b>.",
        "<b>Settings → Video</b>: Base and Output resolution <b>1920×1080</b>, frame rate <b>30</b>.",
        "<b>Settings → Output → Recording</b>: quality <b>High Quality, Medium File Size</b>, format <b>MP4</b>. "
        "If your version only offers MKV, use <b>File → Remux Recordings</b> afterwards to convert to MP4.",
        "In the <b>Sources</b> box click <b>+</b> → <b>Display Capture</b> → choose your monitor. For the "
        "webcam bubble, also add <b>+</b> → <b>Video Capture Device</b> and drag it into a corner.",
        "In the <b>Audio Mixer</b>, the <b>Mic/Aux</b> bar should move when you talk; aim for the yellow zone, "
        "never red. Right-click Mic/Aux → <b>Filters</b> → <b>+</b> → <b>Noise Suppression</b>.",
        "<b>Settings → Hotkeys</b>: set keys for Start, Stop and Pause recording, e.g. "
        f"{key('Ctrl + F9')} / {key('Ctrl + F10')} / {key('Ctrl + F11')}.",
        "Recordings are saved to your <b>Videos</b> folder (change it under Settings → Output).",
    ]),
    CondPageBreak(90 * mm),
]

# ---------------------------------------------------------------- 3. prep
story += [
    P("3. Prepare your PC and accounts", "h1"),
    P("Do this once, before recording either video. Most of it is about making your screen look exactly like a "
      "student's, and keeping private things off camera."),
    P("Test account and files", "h2"),
    *checklist([
        "<b>Create a new Google account just for recording</b>, one that has never used Colab. Then the "
        "first-time screens that students will see (installing Colaboratory in Drive, the Drive permission "
        "screens) appear in your video too.",
        "<b>Use a separate Chrome profile</b> for it: profile icon top right → <b>Add</b>. No personal "
        f"bookmarks, history or autofill on screen. Hide the bookmarks bar with {key('Ctrl + Shift + B')}.",
        f"<b>Build a fresh zip</b> in the repo: {key('python make_student_zip.py')}. To reach it from Windows, type "
        f"{WSL} in File Explorer's address bar, open your Linux distribution, then "
        f"{key('home/ioannis/repos/python-text-analytics-lab/dist')}, and copy {key('python_lab.zip')} to a "
        "Windows folder.",
        "<b>Put the zip where students will get it</b>: ideally a test copy of the course page on the university "
        "platform, so Video 1 shows the real thing. If that isn't possible, start from the zip in Downloads and "
        "show the platform page as a still image.",
        "<b>Empty the test account's Drive</b> and clean your Desktop and Downloads folder: both appear in "
        "Video 1.",
        "<b>Make three simple slides</b> for Video 1's welcome (Scenes 1 to 3): PowerPoint or Google Slides, "
        "plain background, large text. The suggested text is in the shot list. Record them full screen in "
        "slideshow mode.",
        "<b>Optional webcam</b> for the welcome scenes only, as a small bubble in a corner of the slides: seeing "
        "your face once makes the course feel less anonymous. Clipchamp: <b>Screen and camera</b>. OBS: add a "
        "<b>Video Capture Device</b> source.",
    ]),
    box([
        P("<b>Order matters: record Video 1 first, then Video 2, with the same account.</b> Lab 01 never "
          "connects to Drive, so after Video 1 the account still hasn't granted Drive access, and Video 2 can "
          "show the full first-time permission screens. Don't run any lab's Drive cell in between.", "cell"),
        Spacer(1, 3),
        P("Need to retake that part of Video 2? Remove the access at <b>myaccount.google.com → Security → "
          "Your connections to third-party apps &amp; services</b> (the entry is likely named "
          "<i>Google Drive for desktop</i>), and the screens appear again.", "cell"),
    ], WARN_BG, WARN_RULE),
    P("Screen", "h2"),
    *checklist([
        "Display resolution <b>1920×1080</b> (Settings → System → Display), scale 100% or 125%.",
        f"Browser zoom <b>125%</b> in Colab and Drive ({key('Ctrl + +')}). Test: record 10 seconds and watch it on "
        "your phone. Can you read the code?",
        "Bigger mouse pointer: Settings → Accessibility → <b>Mouse pointer and touch</b> → size 2 or 3.",
        "<b>Do not disturb</b> on (Settings → System → Notifications). Close Outlook, Teams and messaging apps.",
    ]),
    P("Colab", "h2"),
    *checklist([
        "<b>Decide the interface language.</b> Students with a Greek Google account see Greek menus (e.g. "
        "<b>Αρχείο</b> instead of <b>File</b>). Either set the test account to the language most students use "
        "(myaccount.google.com → Personal info → Language), or add an on-screen caption with both names each "
        "time you click a menu.",
        "<b>AI features.</b> Colab can show AI code suggestions and an “Explain error” button. Look in "
        "<b>Tools → Settings</b> and turn them off for the recording, or decide what you want to tell students "
        "about them.",
    ]),
    P("Sound", "h2"),
    *checklist([
        "Use a headset or USB microphone rather than the laptop's built-in one, if you can.",
        "A small room with curtains, carpet or a sofa sounds much better than an empty, echoing one.",
        "Make a 10-second test recording and listen back with headphones before you start for real.",
    ]),
    CondPageBreak(120 * mm),
]

# ---------------------------------------------------------------- 4. method
story += [
    P("4. How to record", "h1"),
    grid([
        ["Habit", "Why"],
        ["<b>One scene = one recording.</b> Stop after each scene in the shot list.",
         "A mistake only costs you that scene, and the clips are easy to reorder or replace later."],
        ["<b>Narrate while you click</b> (recommended), reading loosely from the SAY column.",
         "Sounds natural and halves the work. The alternative, recording silently and adding a voice-over in "
         "Clipchamp afterwards, sounds cleaner but takes about twice as long."],
        ["<b>Keep the script in view</b>: print sections 5 and 6, or open them on a second screen or tablet.",
         "You can glance at the next step without switching windows on camera."],
        ["<b>Two seconds of silence</b>, mouse still, at the start and end of every clip.",
         "Gives you clean cut points when editing."],
        ["<b>Stumbled? Pause two seconds and say the sentence again.</b> Don't restart the scene.",
         "You cut the bad take out in editing; nobody will notice."],
        ["<b>Move the mouse slowly</b> and rest on a button for a second before clicking it.",
         "Viewers follow the pointer. Fast jumps lose them."],
        ["<b>Keep recording through waits</b> (uploads, “Connecting…”).",
         "Cut most of the wait when editing, but keep a second or two so students know a pause is normal."],
        ["<b>Speak to one student</b>, at a calm pace, and use “you”.",
         "The videos are for nervous beginners; a friendly tone matters more than perfect wording."],
    ], [0.47, 0.53]),
    Spacer(1, 10),
    box([
        P("<b>Reading the shot lists</b>", "cell"),
        Spacer(1, 3),
        P("Each scene has a blue header with its target timing, the <b>ON SCREEN</b> steps on the left (do them "
          "in order) and what to <b>SAY</b> on the right. Amber boxes are things that may or may not happen on "
          "your screen, with what to say if they do. The timings are a guide only: a scene that runs 20 seconds "
          "longer is fine.", "cell"),
    ]),
    PageBreak(),
]

# ---------------------------------------------------------------- 5. video 1
story += [
    P("5. Shot list · Video 1: Setting up and opening your first lab", "h1"),
    box([P("<b>Starting state:</b> the three welcome slides open in slideshow mode; test Chrome profile open "
           "on the platform's course page; the test account's Drive is empty; Desktop and Downloads are tidy; "
           "recording tool ready.", "cell")]),
    Spacer(1, 8),
    scene(1, "Welcome", "0:00–0:40",
          ["<b>Slide 1</b> (optionally with your webcam in a corner):<br/>"
           "Digital Skills and Business Decision-Making Using Python<br/>"
           "Centre of Continuing Education and Lifelong Learning, University of Piraeus<br/>"
           "Giannis, PhD candidate, University of Piraeus"],
          ["Hello, and welcome! My name is Giannis, and I'm a PhD candidate at the University of Piraeus. Welcome "
           "to Digital Skills and Business Decision-Making Using Python, a course offered by the Centre of "
           "Continuing Education and Lifelong Learning of the University of Piraeus.",
           "This course is for undergraduate and postgraduate economics students, recent graduates, job seekers, "
           "and working professionals who want to build basic programming and data analysis skills. You don't "
           "need any programming experience at all: we start from zero."]),
    scene(2, "What you'll learn", "0:40–1:10",
          ["<b>Slide 2</b>, “What you'll learn”:<br/>"
           "• Write, understand and fix Python code<br/>"
           "• Load, clean, explore and visualize a real dataset with pandas and NumPy<br/>"
           "• Text as the running example, preparing you for <i>Text Analytics with Python</i>"],
          ["By the end of the course, you'll be able to write, understand and fix your own Python code, and to "
           "load, clean, explore and visualize a real dataset with two of Python's most widely used libraries, "
           "pandas and NumPy.",
           "Our focus is data analysis, not software engineering. And we use text, such as customer reviews, as "
           "our running example, so that afterwards you're ready to follow the module Text Analytics with "
           "Python."]),
    scene(3, "How the course works", "1:10–2:00",
          ["<b>Slide 3</b>, “How the course works”:<br/>"
           "• Fully online and self-paced, in Google Colab: nothing to install<br/>"
           "• Weeks 1 to 10: five units of two weeks each, study material and lab exercises (70 hours)<br/>"
           "• Weeks 11 and 12: final project on a real dataset of reviews (20 hours)<br/>"
           "• In total: 12 weeks, 90 hours",
           "Switch to the platform's course page."],
          ["The course runs entirely online and is self-paced: there are no live sessions, so you study whenever "
           "it suits you. Everything runs in Google Colab, in your browser, so there's nothing to install.",
           "It lasts 12 weeks, about 90 hours in total. The first ten weeks are five units of two weeks each, "
           "combining study material with hands-on lab exercises. In the last two weeks you bring it all "
           "together in a final project: your own analysis of a real dataset of customer reviews.",
           "One more thing about this platform: we use it only to share the course material, which you download "
           "from here, together with a few short videos like this one to help you along the way. The actual "
           "work happens in Colab."]),
    scene(4, "What this video covers", "2:00–2:15",
          ["Title card “Setting up the course labs” over the platform's course page (add it when editing)."],
          ["Every lab in this course is a Jupyter notebook that you run in Google Colab, for free. In the rest of "
           "this video, you'll set everything up once, open your first lab, and run your first line of Python. "
           "All you need is a Google account."]),
    scene(5, "Download and unzip", "2:15–2:55",
          ["On the platform, click <b>python_lab.zip</b> to download it.",
           "Open the Downloads folder. Right-click the zip → <b>Extract All</b> → <b>Extract</b>. "
           "(Add a caption when editing: “Mac: double-click”.)",
           "Open the new <b>python_lab</b> folder: <b>labs</b>, <b>data</b>, <b>README.txt</b>. Open "
           "<b>labs</b> briefly to show the 16 lab folders."],
          ["Download the course zip from the platform and unzip it. On Windows, right-click, Extract All. On a "
           "Mac, just double-click. You get a folder called python_lab. Inside, “labs” has one folder per lab, "
           "and “data” has the datasets we'll analyse later.",
           "Don't try to open the notebooks on your computer: we're going to put this folder in Google Drive."]),
    scene(6, "Upload the folder to Google Drive", "2:55–3:45",
          ["Go to <b>drive.google.com</b> (signed in with the test account).",
           "Click <b>+ New</b> → <b>Folder upload</b>. Select the unzipped <b>python_lab</b> folder.",
           "The browser asks to confirm uploading 19 files. Confirm.",
           "Wait for the upload panel (bottom right) to finish. Show <b>python_lab</b> in My Drive."],
          ["Now go to Google Drive. Click New, then Folder upload, and pick the python_lab folder. Make sure it's "
           "the folder, not the zip file: Drive can't open zip files.",
           "Your browser asks you to confirm, and after a few seconds the whole course is in your Drive. You only "
           "do this once."]),
    scene(7, "Open Lab 01 in Colab", "3:45–4:25",
          ["In Drive open <b>python_lab → labs → lab01_setup_basics</b>.",
           "Right-click <b>lab01_student.ipynb</b> → <b>Open with</b> → <b>Google Colaboratory</b>.",
           "The notebook opens in a new tab."],
          ["Open the folder, then labs, then the Lab 01 folder. Right-click the notebook and choose Open with, "
           "Google Colaboratory.",
           "If you don't see Colaboratory in that list, choose Connect more apps, search for Colaboratory, and "
           "install it. You only need to do that once."],
          note="<b>If Google Colaboratory isn't in the Open with list</b> (likely on a brand-new account): keep it "
               "in the recording. Choose <b>Open with → Connect more apps</b>, search “Colaboratory”, click "
               "<b>Install</b>, then open the file again."),
    scene(8, "A quick tour", "4:25–5:05",
          ["Hover over a <b>text cell</b> (the welcome text).",
           "Hover over a grey <b>code cell</b>.",
           "Click the <b>Table of contents</b> icon in the left sidebar to show the lab's sections.",
           "Point at the <b>Connect</b> button / RAM and Disk indicator, top right."],
          ["A notebook is made of cells. Text cells hold the explanations: you just read them. The grey boxes are "
           "code cells: these you run.",
           "On the left, the table of contents lets you jump between sections of the lab. And top right is your "
           "connection to the computer that actually runs your code. It's a machine Google lends you for free, "
           "not your own laptop."]),
    scene(9, "Run the first cell", "5:05–5:45",
          ["Scroll to section 1. Click the <b>print(\"Hello there! General Kenobi!\")</b> cell.",
           "Hover so the <b>▶</b> button appears, then click it. Let the “Connecting” wait play out.",
           "Point at the output and at the number in brackets on the left.",
           f"Run the next code cell with {key('Shift + Enter')}."],
          ["Click a code cell and press the play button on its left. The very first run takes a few seconds, "
           "because Colab is starting your machine. There's the output, right under the cell.",
           "The faster way is Shift and Enter: it runs the cell and moves you to the next one. That's how you'll "
           "move through every lab."],
          note="<b>If a “This notebook was not authored by Google” warning appears</b>, keep it and say: "
               "“If you see this warning, click Run anyway. Our labs are safe to run.”"),
    scene(10, "Cells share memory, and Colab forgets", "5:45–6:55",
          ["In “Cells Share a Memory”, run <b>x = 5</b>, then <b>print(\"x plus ten is\", x + 10)</b>. "
           "Output: 15.",
           "<b>Runtime → Restart session</b>, and confirm.",
           "Run only the second cell. Show <b>NameError: name 'x' is not defined</b>.",
           "Click the second cell, then <b>Runtime → Run before</b>. Run it again: it works."],
          ["Cells share one memory: the x created in the first cell is available in the second. But that memory "
           "is temporary. If you close the tab, take a long break, or restart, Colab forgets every variable.",
           "Watch: I restart, run the second cell, and Python has never heard of x. Your code is still there; only "
           "the memory is gone.",
           "The fix is to re-run the cells above, and Runtime, Run before does exactly that in one click. Remember "
           "it: whenever something is “not defined”, run the cells before it."]),
    scene(11, "Errors are normal", "6:55–7:20",
          ["Run the <b>print(mesage)</b> cell.",
           "Point at the line number in the traceback, the <b>NameError</b>, and the “Did you mean: "
           "'message'?” hint."],
          ["You're going to see a lot of red. That's fine. Every error tells you which line broke and why. Here "
           "it's line 2, a NameError, and Python even guesses what you meant. The lab shows you how to read "
           "these, so take your time with that part."]),
    scene(12, "Exercises, saving, and next week", "7:20–8:10",
          ["Jump to section 4 with the table of contents. Click the Exercise 1 <b># TODO</b> cell, type "
           "<b>name = \"Alex\"</b>, run it.",
           f"Press {key('Ctrl + S')}.",
           "Switch to the Drive tab: <b>lab01_student.ipynb</b> is still in "
           "<b>python_lab/labs/lab01_setup_basics</b>."],
          ["At the end of each lab there are exercises. Cells marked TODO are yours: click in, write your code, "
           "run it. Because you opened this lab from your Drive, Colab saves every change straight back into that "
           "file. Ctrl+S saves right away if you want to be sure.",
           "Next week, do exactly the same: go to your python_lab folder in Drive, open the next lab's folder, and "
           "open it with Colab. No more downloading or uploading. See you in the lab."]),
    PageBreak(),
]

# ---------------------------------------------------------------- 6. video 2
story += [
    P("6. Shot list · Video 2: Loading the course data", "h1"),
    box([P("<b>Starting state:</b> same test account, Video 1 already recorded, <b>no Drive cell run yet</b>. "
           "Open Lab 08 from Drive, scroll to <b>Part 5</b>, click its first code cell (the one starting "
           "<b># Connect to your Google Drive</b>) and choose <b>Runtime → Run before</b>, so every earlier cell "
           "has run but the Drive cell hasn't. Close the Files panel.", "cell")]),
    Spacer(1, 8),
    scene(1, "Intro", "0:00–0:20",
          ["Title card “Loading the course data”.",
           "Drive tab: the <b>python_lab</b> folder, opened on <b>data</b>."],
          ["From Lab 08 on, we work with real customer reviews. They're already in your Drive: they're in the data "
           "folder you uploaded with the labs. This video shows how a lab gets to them, and what to do when Colab "
           "asks for permission."]),
    scene(2, "Run the Drive cell", "0:20–1:30",
          ["Lab 08, Part 5: run the cell starting <b># Connect to your Google Drive and find the course's data "
           "folder.</b>",
           "Popup “Permit this notebook to access your Google Drive files?” → <b>Connect to Google Drive</b>.",
           "Choose the Google account.",
           "On Google's permission screen, if there are checkboxes, tick <b>Select all</b>, then "
           "<b>Continue</b>.",
           "Point at the output: <b>Mounted at /content/drive</b> and <b>Course data folder: "
           "/content/drive/MyDrive/python_lab/data</b>."],
          ["Every lab that uses data has this cell. It connects the notebook to your Google Drive and finds the "
           "course's data folder. The first time you run it in a session, Colab asks for permission.",
           "Click Connect to Google Drive, choose your account, and allow access. If Google shows you a list of "
           "checkboxes, tick all of them. If you skip some, the connection fails, and you'll just have to run the "
           "cell again.",
           "When it's done, it prints where it found the data. You don't need to understand this cell's code yet: "
           "just run it and allow access."]),
    scene(3, "Where the data is", "1:30–2:10",
          ["Click the <b>folder icon</b> in the left sidebar. Open <b>drive → MyDrive → python_lab → data</b>. "
           "Point at <b>reviews_sample.txt</b>.",
           "Run the next code cell. Output: <b>Loaded 600 reviews.</b>"],
          ["Open the Files panel on the left. Your Drive now appears in it, under drive, MyDrive. There's our data "
           "folder, and the file of 600 reviews. The next cell reads it, using the file skills from Lab 07.",
           "Remember from Lab 07: files your code writes in the top-level folder here are temporary. Files inside "
           "drive are your real Google Drive, and they stay."]),
    scene(4, "After a break", "2:10–3:20",
          ["<b>Runtime → Disconnect and delete runtime</b>, and confirm.",
           "Click a cell further down Part 5 that uses <b>reviews</b> and run it. It reconnects, then fails: "
           "<b>NameError: name 'reviews' is not defined</b>.",
           "With that cell selected: <b>Runtime → Run before</b>. The Drive popup appears again: Connect to "
           "Google Drive, choose the account.",
           "Run the cell again: it works."],
          ["Here's what happens after a long break. Colab takes back the machine. I'm doing it on purpose with "
           "Disconnect and delete runtime.",
           "Now I run a cell further down, and: “reviews is not defined”. Nothing is lost: your notebook and the "
           "data are safe in your Drive. Colab just forgot the connection and the variables.",
           "The fix is the same as always: click the cell, then Runtime, Run before. Colab runs everything above "
           "it, asks for Drive access again, which is quicker this time, and you carry on."]),
    scene(5, "If the data can't be found", "3:20–3:45",
          ["Show a still image (or a caption) of the cell's error: <b>Couldn't find the course's 'data' folder "
           "in your Google Drive…</b>",
           "Tip: to capture it, temporarily rename the <b>data</b> folder in the test Drive, run the cell, take a "
           "screenshot, then rename it back."],
          ["If this cell ever says it couldn't find the data folder, the data isn't in your Drive. Usually the zip "
           "file was uploaded instead of the unzipped folder. Upload the unzipped python_lab folder to My Drive "
           "and run the cell again."]),
    scene(6, "Wrap-up", "3:45–4:00",
          ["Back on the Lab 08 notebook."],
          ["That's it. Every lab with data starts with this cell. Run it, allow access, and the data is there. "
           "Back to the lab."]),
    PageBreak(),
]

# ---------------------------------------------------------------- 7-8. edit, publish, checklist
story += [
    P("7. Edit the videos", "h1"),
    P("The steps below use Clipchamp. Any editor (Shotcut, DaVinci Resolve, iMovie) has the same tools under "
      "similar names."),
    grid([
        ["Step", "How", "Tip"],
        ["<b>1 · Put the clips in order</b>",
         "If you recorded in Clipchamp they're already on the timeline. Otherwise drag your files from "
         "<b>Your media</b> onto the timeline, scene 1 first.",
         "Name OBS files as you go (v1-s3.mp4) so the order is obvious."],
        ["<b>2 · Trim</b>",
         "Click a clip and drag its edges to cut the start and end. Use the <b>split</b> tool (scissors) to cut "
         "out a bad take or a long wait in the middle, then delete the piece.",
         "Cut most of each wait but leave a second or two."],
        ["<b>3 · Title card</b>",
         "<b>Text</b> → pick a plain title → type “Setting up the course labs” (or “Loading the course data”). "
         "About 3 seconds, at the start of Scene 4 in Video 1 and at the start of Video 2.",
         "Keep the same style for both videos and the welcome slides."],
        ["<b>4 · Point at small things</b>",
         "Add an arrow or circle from the graphics/stickers panel over tiny targets: the ▶ button, the folder "
         "icon, the Runtime menu.",
         "Only where the pointer alone isn't enough."],
        ["<b>5 · Captions</b>",
         "<b>Captions</b> → turn on <b>auto captions</b> → choose the narration language, then read them through "
         "and fix mistakes.",
         "Check that your narration language is in the list. Captions help students who watch without sound."],
        ["<b>6 · No background music</b>", "Leave the narration on its own.", "Music competes with the voice."],
        ["<b>7 · Export</b>",
         "<b>Export → 1080p</b>. Save as e.g. <b>python_lab_video1_setup.mp4</b> and "
         "<b>python_lab_video2_data.mp4</b>.",
         "Watch the whole export once, with sound, before publishing."],
    ], [0.22, 0.48, 0.30]),
    Spacer(1, 12),
    P("8. Publish", "h1"),
    *bullets([
        "<b>Choose where the videos live.</b> Either upload the MP4 files to the university platform (check its "
        "file-size limit; an 8-minute 1080p video is usually 150–250 MB), or upload them to YouTube as "
        "<b>Unlisted</b> (only people with the link can see them) and share the links.",
        f"<b>Paste the two links</b> into {key('onboarding/platform_text.md')} in place of "
        f"{key('[link to video 1]')} and {key('[link to video 2]')}, then put that text on the platform next to "
        "the zip.",
        "<b>Test as a student would:</b> open the platform page in a private/incognito window, click both links, "
        "and check that the videos play with sound.",
        "<b>Review every semester.</b> Re-record a scene if Colab or Drive change their screens noticeably, or "
        "if the zip's folder structure changes. Thanks to one-scene-per-clip, that's usually a single short "
        "retake.",
    ]),
    PageBreak(),
    P("Final checklist", "h1"),
    P("Tick these off as you go. Print this page and keep it next to your keyboard."),
    Spacer(1, 4),
    box([
        *checklist([
            "Recording tool chosen and tested with a 10-second clip (sound checked on headphones).",
            "Test Google account + separate Chrome profile; Drive empty; Do not disturb on.",
            "Fresh zip built and placed on the platform (or in Downloads).",
            "Three welcome slides ready; webcam decided.",
            "Interface language and AI features decided.",
            "Video 1 recorded, then Video 2 (no Drive cell run in between).",
            "Both videos trimmed, titled, captioned and exported at 1080p.",
            "Videos uploaded; links pasted into the platform text; links tested in a private window.",
        ]),
    ]),
]

if __name__ == "__main__":
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                            bottomMargin=17 * mm, title="Recording the Colab Onboarding Videos",
                            author="Ioannis Nikolaidis", subject="Instructor guide for the onboarding videos")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("wrote", OUT)
