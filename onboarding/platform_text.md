# Text for the university platform

Paste the section below into the platform, next to `python_lab.zip`. Replace the
two `[link to video ...]` placeholders once the videos are uploaded.

---

## How to set up the course labs

All labs are Jupyter notebooks that you run in **Google Colab**, for free, in your browser. You need a Google account. You set things up once, at the start of the course:

1. **Download** `python_lab.zip` from this page.
2. **Unzip it** on your computer.
   - Windows: right-click the file → *Extract All* → *Extract*.
   - Mac: double-click the file.

   You now have a folder called `python_lab` containing `labs`, `data` and `README.txt`.
3. **Upload the whole folder to Google Drive.** Go to [drive.google.com](https://drive.google.com), click **+ New → Folder upload**, and select the `python_lab` folder. Upload the unzipped folder, not the `.zip` file.
4. **Open a lab.** In Google Drive, go to `python_lab → labs → lab01_setup_basics`, right-click `lab01_student.ipynb` and choose **Open with → Google Colaboratory**.

From then on, open every lab the same way, from the `python_lab` folder in your Drive. Colab saves your work straight back into that file.

Video walkthroughs:
- Setting up and opening your first lab (watch before Lab 01): [link to video 1]
- Loading the course data (watch before Lab 08): [link to video 2]

### If something goes wrong

| What you see | What to do |
|---|---|
| No *Google Colaboratory* under *Open with* | Choose *Open with → Connect more apps*, search for **Colaboratory**, install it, then try again. |
| `Couldn't find the course's 'data' folder in your Google Drive` | The `data` folder isn't in your Drive. Check that you unzipped the course files and uploaded the whole `python_lab` folder (not the `.zip`) to *My Drive*. |
| An error mentioning `credential propagation was unsuccessful` | When Colab asked for access to your Drive, not every permission was ticked. Run the cell again and tick **all** the checkboxes (or *Select all*). |
| `NameError: name '...' is not defined` | Colab forgot your earlier cells (after a break, or after closing the tab). Click the cell, then **Runtime → Run before**, and run it again. |
