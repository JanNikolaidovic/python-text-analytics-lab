## What this repo is

Course materials (Jupyter notebooks) for the Python Text Analytics Lab, University of Piraeus, Department of Economics. Students download the course as a zip from the university platform, upload the unzipped folder to their Google Drive, and open the notebooks in Google Colab from there. The GitHub repo is private and is never seen by students.

## Labs

| Lab | Topic | Student notebook |
|---|---|---|
| 01 | Getting Started with Jupyter Notebooks in Google Colab | `labs/lab01_setup_basics/lab01_student.ipynb` |
| 02 | Variables & Simple Data Types (Part 1: Strings) | `labs/lab02_variables_data_types_part1/lab02_student.ipynb` |
| 03 | Variables & Simple Data Types (Part 2: Numbers & Operations) | `labs/lab03_variables_data_types_part2/lab03_student.ipynb` |
| 04 | Data Structures | `labs/lab04_data_structures/lab04_student.ipynb` |
| 05 | Control Flow | `labs/lab05_control_flow/lab05_student.ipynb` |
| 06 | Functions | `labs/lab06_functions/lab06_student.ipynb` |
| 07 | Files & Exceptions | `labs/lab07_files_exceptions/lab07_student.ipynb` |
| 08 | Text Processing Toolkit | `labs/lab08_text_processing/lab08_student.ipynb` |
| 09 | Regular Expressions for Text Cleaning | `labs/lab09_regular_expressions/lab09_student.ipynb` |
| 10 | Text as Vectors | `labs/lab10_text_as_vectors/lab10_student.ipynb` |
| 11 | NumPy | `labs/lab11_numpy/lab11_student.ipynb` |
| 12 | pandas I: Loading and Selecting Data | `labs/lab12_pandas_loading_selecting/lab12_student.ipynb` |
| 13 | pandas II: Cleaning Text Data | `labs/lab13_pandas_cleaning/lab13_student.ipynb` |
| 14 | pandas III: Grouping and the Dependent Variable | `labs/lab14_pandas_grouping_dv/lab14_student.ipynb` |
| 15 | Data Visualization with Matplotlib and Seaborn | `labs/lab15_visualization/lab15_student.ipynb` |
| 16 | Exploratory Data Analysis End to End | `labs/lab16_eda_end_to_end/lab16_student.ipynb` |

## Data

`data/` holds the course's running dataset. It ships to students inside the zip, next to `labs/`. Labs 08, 09 and 11-16 load it with a standard "find the course data" cell: in Colab it mounts the student's Google Drive and searches up to three folder levels below My Drive for `data/womens_clothing_ecommerce_reviews.csv` (so a renamed or double-nested course folder still works); outside Colab it looks in `../../data`, which is the repo's `data/` when you run a master locally. The cell sets `DATA_DIR`; the pandas labs then use `DATA_PATH = f"{DATA_DIR}/womens_clothing_ecommerce_reviews.csv"`. See [data/README.md](data/README.md) for source and licence.

## Setup

```bash
source .venv/bin/activate
```

`.venv` already contains the dependencies (nbformat, nbstripout, jupyter, etc.). `requirements.txt` is a `pip freeze` of the venv (the venv remains the source of truth). Labs 11+ use numpy, pandas, matplotlib and seaborn, which are preinstalled in Colab, so no install cell is needed.

## The master/student build pipeline

This is the core mechanic of the repo and the main thing to get right:

```
solutions/labNN_<slug>/labNN.ipynb          ← MASTER. The only file ever edited by hand.
labs/labNN_<slug>/labNN_student.ipynb       ← GENERATED. Never edit by hand.
build_labs.py                               ← strips solution cells to produce the student version
new_lab.py                                  ← scaffolds a new master notebook
make_student_zip.py                         ← rebuilds every student notebook and packs dist/python_lab.zip
```

**Golden rule: edit only under `solutions/`.** Files under `labs/` are overwritten by `build_labs.py` and hand edits there are silently lost.

- A code cell is a "solution" cell (stripped from the student build) if its first non-empty line is exactly `# @solution`, or it carries the notebook metadata tag `solution` (see `is_solution()` in [build_labs.py](build_labs.py)).
- Common pattern: a `# TODO` cell for students immediately followed by a `# @solution` cell with the answer.

### Common commands

Create a new lab (scaffolds `solutions/labNN_<slug>/labNN.ipynb`):
```bash
python new_lab.py 02 data_structures "Data Structures & Control Flow"
```

Build the student notebook(s) from a master after editing:
```bash
python build_labs.py solutions/lab02_data_structures/lab02.ipynb
```

Rebuild everything after a global change:
```bash
python build_labs.py solutions/*/lab*.ipynb
```

Package the course for the university platform (rebuilds all student notebooks, then writes `dist/python_lab.zip`):
```bash
python make_student_zip.py
```

After building, commit `labs/` and `solutions/` together. Students only ever see what's in the zip, so a change isn't live for them until you rerun `python make_student_zip.py` and upload the new `dist/python_lab.zip` to the platform (the zip never contains `solutions/` or outputs).

## Notebook conventions

- Every answer cell must start with `# @solution` as its literal first line.
- Notebook outputs are stripped on commit via the `nbstripout` git filter (configured in local git config, `.venv/bin/python3 -m nbstripout`) — the repo stores only code/text, keeping diffs readable.
- Level 2+ labs that require installs should pin versions in a top install cell (e.g. `!pip install -q bertopic==0.16.0`) so notebooks don't break in future semesters.
- Students open every lab from their course folder in Google Drive, so Colab saves their work in place; Lab 01 sets up this habit. Runtimes are still ephemeral, so variables and files written to `/content` disappear.
- A lab that needs the dataset starts its data section with the standard Drive cell (copy it verbatim from any of labs 08-16) and reads files via `DATA_DIR`. Never load data from a URL: the repo is private.
- New labs need their row added to `README.md` in addition to the build step.

Full step-by-step workflow (creating vs. modifying labs, checklists) is in [WORKFLOW.md](WORKFLOW.md) — consult it for the exact sequence when doing lab authoring work.
