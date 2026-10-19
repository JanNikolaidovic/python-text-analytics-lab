# Video 2: Loading the Course Data

**When students watch it:** before Lab 08 (the first lab that loads the course data). Worth relinking at Lab 12, where the full dataset first appears.
**Target length:** about 4 minutes.
**Goal:** students can connect a lab to their Google Drive (including the permission screens), know where the data lives, and recover after a reset.

## Before recording

- Use the same test account as Video 1, with `python_lab` already in its Drive.
- Make sure this account has **not** yet granted Colab access to Drive, so the full permission flow is recorded.
- Open Lab 08 from Drive and run every cell above Part 5, so the earlier functions exist.
- Same UI language and AI-feature checks as Video 1.

## Script

### Scene 1: Intro (0:00 to 0:20)

**Show:** title card "Loading the course data", then the `python_lab` folder in Drive, opened on `data`.

**Say:**
> From Lab 08 on, we work with real customer reviews. They're already in your Drive: they're in the data folder you uploaded with the labs. This video shows how a lab gets to them, and what to do when Colab asks for permission.

### Scene 2: Run the Drive cell (0:20 to 1:30)

**Show:**
1. Lab 08, Part 5. Run the cell starting `# Connect to your Google Drive and find the course's data folder.`
2. The popup "Permit this notebook to access your Google Drive files?" → **Connect to Google Drive**.
3. Choose the Google account.
4. On Google's permission screen, if there are checkboxes, tick **Select all**, then **Continue**.
5. Output: `Mounted at /content/drive` and `Course data folder: /content/drive/MyDrive/python_lab/data`.

**Say:**
> Every lab that uses data has this cell. It connects the notebook to your Google Drive and finds the course's data folder. The first time you run it in a session, Colab asks for permission. Click Connect to Google Drive, choose your account, and allow access. If Google shows you a list of checkboxes, tick all of them. If you skip some, the connection fails, and you'll just have to run the cell again.
>
> When it's done, it prints where it found the data. You don't need to understand this cell's code yet: just run it and allow access.

### Scene 3: Where the data is (1:30 to 2:10)

**Show:**
1. Click the **folder icon** in the left sidebar. Open `drive → MyDrive → python_lab → data`. Point at `reviews_sample.txt`.
2. Run the next cell; output `Loaded 600 reviews.`

**Say:**
> Open the Files panel on the left. Your Drive now appears in it, under drive, MyDrive. There's our data folder, and the file of 600 reviews. The next cell reads it, using the file skills from Lab 07.
>
> Remember from Lab 07: files your code writes in the top-level folder here are temporary. Files inside drive are your real Google Drive, and they stay.

### Scene 4: After a break (2:10 to 3:20)

**Show:**
1. **Runtime → Disconnect and delete runtime**, confirm.
2. Click a cell further down Part 5 that uses `reviews` and run it. It reconnects, then fails: `NameError: name 'reviews' is not defined`.
3. With that cell selected, **Runtime → Run before**. The Drive popup appears again: Connect to Google Drive, choose account. The cells run.
4. Run the cell again: it works.

**Say:**
> Here's what happens after a long break. Colab takes back the machine. I'm doing it on purpose with Disconnect and delete runtime. Now I run a cell further down, and: "reviews is not defined". Nothing is lost: your notebook and the data are safe in your Drive. Colab just forgot the connection and the variables.
>
> The fix is the same as always: click the cell, then Runtime, Run before. Colab runs everything above it, asks for Drive access again, which is quicker this time, and you carry on.

### Scene 5: If the data can't be found (3:20 to 3:45)

**Show:** a still image or caption of the cell's error message: `Couldn't find the course's 'data' folder in your Google Drive...`

**Say:**
> If this cell ever says it couldn't find the data folder, the data isn't in your Drive. Usually the zip file was uploaded instead of the unzipped folder. Upload the unzipped python_lab folder to My Drive and run the cell again.

### Scene 6: Wrap-up (3:45 to 4:00)

**Say:**
> That's it. Every lab with data starts with this cell. Run it, allow access, and the data is there. Back to the lab.
