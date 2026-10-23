# Video 1: Setting Up and Opening Your First Lab

**When students watch it:** before Lab 01. Link it next to `python_lab.zip` on the platform.
**Target length:** about 8 minutes (2 minutes of welcome and course overview, then 6 minutes of setup).
**Goal:** students know who you are and how the course works, and a student who has never used Colab gets from the platform to a running Lab 01, knows how to recover after a reset, and knows how to find the lab again next week.

## Before recording

- Prepare **three simple slides** for Scenes 1 to 3 (PowerPoint or Google Slides, plain background, large text). Suggested content is under each scene. Record them full screen in slideshow mode.
- Optional: turn on your **webcam** for Scenes 1 to 3 only (a small bubble in a corner of the slides). Seeing your face once makes the course feel less anonymous; the rest of the video works fine without it. In Clipchamp choose *Screen and camera*; in OBS add a *Video Capture Device* source.
- Build a fresh zip with `python make_student_zip.py` and put it on the platform (or a test copy of the course page).
- Use a **new Google account** that has never used Colab, so the recording shows exactly what students will see the first time (including any "Connect more apps" step). This also keeps personal files off screen.
- Zoom the browser to 125% so code is readable on a phone.
- UI language: students with a Greek Google account will see Greek menus (e.g. *Αρχείο* instead of *File*). Record in the language most students will use, or add captions with both names for each menu item you click.
- Check Colab's AI features (inline code suggestions, "Explain error" button). Turn them off in *Tools → Settings* before recording, or decide what you want to tell students about them.

## Script

### Scene 1: Welcome (0:00 to 0:40)

**Show:** slide 1 (optionally with your webcam in a corner).
- Digital Skills and Business Decision-Making Using Python
- Centre of Continuing Education and Lifelong Learning, University of Piraeus
- Giannis, PhD candidate, University of Piraeus

**Say:**
> Hello, and welcome! My name is Giannis, and I'm a PhD candidate at the University of Piraeus. Welcome to *Digital Skills and Business Decision-Making Using Python*, a course offered by the Centre of Continuing Education and Lifelong Learning of the University of Piraeus.
>
> This course is for undergraduate and postgraduate economics students, recent graduates, job seekers, and working professionals who want to build basic programming and data analysis skills. You don't need any programming experience at all: we start from zero.

### Scene 2: What you'll learn (0:40 to 1:10)

**Show:** slide 2, "What you'll learn".
- Write, understand and fix Python code
- Load, clean, explore and visualize a real dataset with pandas and NumPy
- Text as the running example, preparing you for *Text Analytics with Python*

**Say:**
> By the end of the course, you'll be able to write, understand and fix your own Python code, and to load, clean, explore and visualize a real dataset with two of Python's most widely used libraries, pandas and NumPy.
>
> Our focus is data analysis, not software engineering. And we use text, such as customer reviews, as our running example, so that afterwards you're ready to follow the module *Text Analytics with Python*.

### Scene 3: How the course works (1:10 to 2:00)

**Show:**
1. Slide 3, "How the course works".
   - Fully online and self-paced, in Google Colab: nothing to install
   - Weeks 1 to 10: five units of two weeks each, study material and lab exercises (70 hours)
   - Weeks 11 and 12: final project on a real dataset of reviews (20 hours)
   - In total: 12 weeks, 90 hours
2. Switch to the platform's course page.

**Say:**
> The course runs entirely online and is self-paced: there are no live sessions, so you study whenever it suits you. Everything runs in Google Colab, in your browser, so there's nothing to install.
>
> It lasts 12 weeks, about 90 hours in total. The first ten weeks are five units of two weeks each, combining study material with hands-on lab exercises. In the last two weeks you bring it all together in a final project: your own analysis of a real dataset of customer reviews.
>
> One more thing about this platform: we use it only to share the course material, which you download from here, together with a few short videos like this one to help you along the way. The actual work happens in Colab.

### Scene 4: What this video covers (2:00 to 2:15)

**Show:** title card "Setting up the course labs" over the platform's course page.

**Say:**
> Every lab in this course is a Jupyter notebook that you run in Google Colab, for free. In the rest of this video, you'll set everything up once, open your first lab, and run your first line of Python. All you need is a Google account.

### Scene 5: Download and unzip (2:15 to 2:55)

**Show:**
1. On the platform, the folder with `python_lab.zip`. Click to download it.
2. In the Downloads folder, right-click → *Extract All* → *Extract* (on Windows; add a caption: "Mac: double-click").
3. Open the new `python_lab` folder: `labs`, `data`, `README.txt`. Open `labs` briefly to show the 16 lab folders.

**Say:**
> Download the course zip from the platform and unzip it. On Windows, right-click, Extract All. On a Mac, just double-click. You get a folder called python_lab. Inside, "labs" has one folder per lab, and "data" has the datasets we'll analyse later. Don't try to open the notebooks on your computer: we're going to put this folder in Google Drive.

### Scene 6: Upload the folder to Google Drive (2:55 to 3:45)

**Show:**
1. Go to `drive.google.com`, signed in.
2. Click **+ New → Folder upload**. Select the `python_lab` folder (the unzipped one).
3. The browser asks to confirm uploading 19 files. Confirm.
4. Wait for the upload panel at the bottom right to finish. Show `python_lab` in *My Drive*.

**Say:**
> Now go to Google Drive. Click New, then Folder upload, and pick the python_lab folder. Make sure it's the folder, not the zip file: Drive can't open zip files. Your browser asks you to confirm, and after a few seconds the whole course is in your Drive. You only do this once.

### Scene 7: Open Lab 01 in Colab (3:45 to 4:25)

**Show:** in Drive, open `python_lab → labs → lab01_setup_basics`. Right-click `lab01_student.ipynb` → **Open with → Google Colaboratory**. The notebook opens in a new tab.

If the fresh account doesn't list Google Colaboratory, keep that in the recording: *Open with → Connect more apps*, search "Colaboratory", install, then open the file again.

**Say:**
> Open the folder, then labs, then the Lab 01 folder. Right-click the notebook and choose Open with, Google Colaboratory. If you don't see Colaboratory in that list, choose Connect more apps, search for Colaboratory, and install it. You only need to do that once.

### Scene 8: A quick tour (4:25 to 5:05)

**Show:** hover over each item as you mention it.
1. A text cell (the welcome text).
2. A grey code cell.
3. The **Table of contents** icon in the left sidebar; click it to show the lab's sections.
4. The **Connect** button / RAM-Disk indicator top right.

**Say:**
> A notebook is made of cells. Text cells hold the explanations: you just read them. The grey boxes are code cells: these you run. On the left, the table of contents lets you jump between sections of the lab. And top right is your connection to the computer that actually runs your code. It's a machine Google lends you for free, not your own laptop.

### Scene 9: Run the first cell (5:05 to 5:45)

**Show:** scroll to section 1, click the `print("Hello there! General Kenobi!")` cell. Hover so the ▶ button appears, click it. Let the "Connecting" wait play out (don't cut it). Point at the output and at the number in brackets on the left. Then run the next code cell with **Shift + Enter**.

**Say:**
> Click a code cell and press the play button on its left. The very first run takes a few seconds, because Colab is starting your machine. There's the output, right under the cell. The faster way is Shift and Enter: it runs the cell and moves you to the next one. That's how you'll move through every lab.

If a "This notebook was not authored by Google" warning appears, keep it in and say:
> If you see this warning, click "Run anyway". Our labs are safe to run.

### Scene 10: Cells share memory, and Colab forgets (5:45 to 6:55)

**Show:**
1. In "Cells Share a Memory", run `x = 5`, then `print("x plus ten is", x + 10)`. Output: 15.
2. **Runtime → Restart session**, confirm.
3. Run only the second cell. Show `NameError: name 'x' is not defined`.
4. Click the second cell, then **Runtime → Run before**. Run it again: it works.

**Say:**
> Cells share one memory: the x created in the first cell is available in the second. But that memory is temporary. If you close the tab, take a long break, or restart, Colab forgets every variable. Watch: I restart, run the second cell, and Python has never heard of x. Your code is still there; only the memory is gone. The fix is to re-run the cells above, and Runtime, Run before does exactly that in one click. Remember it: whenever something is "not defined", run the cells before it.

### Scene 11: Errors are normal (6:55 to 7:20)

**Show:** run the `print(mesage)` cell. Highlight the line number in the traceback, the `NameError`, and the "Did you mean: 'message'?" hint.

**Say:**
> You're going to see a lot of red. That's fine. Every error tells you which line broke and why. Here it's line 2, a NameError, and Python even guesses what you meant. The lab shows you how to read these, so take your time with that part.

### Scene 12: Exercises, saving, and next week (7:20 to 8:10)

**Show:**
1. Jump to section 4 with the table of contents. Click the Exercise 1 `# TODO` cell, type `name = "Alex"`, run it.
2. Press **Ctrl + S**.
3. Switch to the Drive tab: show `lab01_student.ipynb` still in `python_lab/labs/lab01_setup_basics`.

**Say:**
> At the end of each lab there are exercises. Cells marked TODO are yours: click in, write your code, run it. Because you opened this lab from your Drive, Colab saves every change straight back into that file. Ctrl+S saves right away if you want to be sure.
>
> Next week, do exactly the same: go to your python_lab folder in Drive, open the next lab's folder, and open it with Colab. No more downloading or uploading. See you in the lab.
