#!/usr/bin/env python3
"""Build the zip that students download from the university platform.

Rebuilds every student notebook from its master first, then writes
dist/python_lab.zip containing (no solutions, no outputs):

    README.txt                                 setup steps for students
    labs/labNN_<slug>/labNN_student.ipynb
    data/womens_clothing_ecommerce_reviews.csv
    data/reviews_sample.txt

There is deliberately no top-level folder inside the zip: Windows "Extract All"
and macOS both create a folder named after the zip, so students end up with a
single python_lab/ folder. Keep labs/ and data/ side by side: the notebooks'
local fallback looks for the data two levels up (../../data).

Usage:
    python make_student_zip.py
"""
import zipfile
from pathlib import Path

import nbformat

from build_labs import build, is_solution, student_path_for

ZIP_PATH = Path("dist/python_lab.zip")
DATA_FILES = ["data/womens_clothing_ecommerce_reviews.csv", "data/reviews_sample.txt"]

README = """\
PYTHON LAB: COURSE FILES
========================

1. Unzip this file on your computer.
   Windows: right-click the .zip file > Extract All > Extract.
   Mac: double-click the .zip file.

2. Upload the unzipped folder to Google Drive.
   Go to drive.google.com, click "+ New" > "Folder upload", and choose the
   unzipped folder (the one that contains "labs" and "data").
   Upload the whole folder, not the .zip file.

3. Open a lab.
   In Google Drive, open the folder, then "labs", then the lab's folder
   (e.g. "lab01_setup_basics"). Right-click the .ipynb file and choose
   Open with > Google Colaboratory.

Always open the labs from this folder in your Google Drive: Colab saves your
work straight back into it. Keep the "labs" and "data" folders together; from
Lab 08 on, the labs read the course data from the "data" folder.

Data source: "Women's E-Commerce Clothing Reviews" by Nick Brooks, published
on Kaggle under a CC0 (Public Domain) licence.
"""


def clean_student_notebook(path: Path) -> str:
    """Return the notebook as JSON with outputs cleared, refusing any solution cell."""
    nb = nbformat.read(path, as_version=4)
    leaked = [i for i, c in enumerate(nb.cells) if is_solution(c)]
    if leaked:
        raise SystemExit(f"{path} still contains solution cells {leaked}; refusing to zip it.")
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    return nbformat.writes(nb)


def main() -> None:
    masters = sorted(Path("solutions").glob("lab*/lab*.ipynb"))
    for master in masters:
        build(str(master))

    ZIP_PATH.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.txt", README)
        for master in masters:
            student = student_path_for(master)
            zf.writestr(student.as_posix(), clean_student_notebook(student))
        for data_file in DATA_FILES:
            zf.write(data_file, data_file)

    print(f"\nWrote {ZIP_PATH} ({ZIP_PATH.stat().st_size / 1e6:.1f} MB, {len(masters)} labs + data)")


if __name__ == "__main__":
    main()
