## What this repo is

Course materials (Jupyter notebooks) for the Python Text Analytics Lab, University of Piraeus, Department of Economics. Students run the notebooks in Google Colab.

## Labs

| Lab | Topic | Student notebook |
|---|---|---|
| 01 | Getting Started with Jupyter Notebooks in Google Colab | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab01_setup_basics/lab01_student.ipynb) |
| 02 | Variables & Simple Data Types (Part 1: Strings) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab02_variables_data_types_part1/lab02_student.ipynb) |
| 03 | Variables & Simple Data Types (Part 2: Numbers & Operations) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab03_variables_data_types_part2/lab03_student.ipynb) |
| 04 | Data Structures | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab04_data_structures/lab04_student.ipynb) |
| 05 | Control Flow | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab05_control_flow/lab05_student.ipynb) |
| 06 | Functions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab06_functions/lab06_student.ipynb) |
| 07 | Files & Exceptions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab07_files_exceptions/lab07_student.ipynb) |
| 08 | Text Processing Toolkit | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab08_text_processing/lab08_student.ipynb) |
| 09 | Regular Expressions for Text Cleaning | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab09_regular_expressions/lab09_student.ipynb) |
| 10 | Text as Vectors | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab10_text_as_vectors/lab10_student.ipynb) |
| 11 | NumPy | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab11_numpy/lab11_student.ipynb) |
| 12 | pandas I: Loading and Selecting Data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab12_pandas_loading_selecting/lab12_student.ipynb) |
| 13 | pandas II: Cleaning Text Data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab13_pandas_cleaning/lab13_student.ipynb) |
| 14 | pandas III: Grouping and the Dependent Variable | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab14_pandas_grouping_dv/lab14_student.ipynb) |
| 15 | Data Visualization with Matplotlib and Seaborn | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab15_visualization/lab15_student.ipynb) |
| 16 | Exploratory Data Analysis End to End | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JanNikolaidovic/python-text-analytics-lab/blob/main/labs/lab16_eda_end_to_end/lab16_student.ipynb) |

## Data

`data/` holds the course's running dataset, loaded by the labs straight from GitHub (raw URLs), so it must be pushed before labs 08+ work in Colab. See [data/README.md](data/README.md) for source and licence.

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
```

**Golden rule: edit only under `solutions/`.** Files under `labs/` are overwritten by `build_labs.py` and hand edits there are silently lost.

- A code cell is a "solution" cell (stripped from the student build) if its first non-empty line is exactly `# @solution`, or it carries the notebook metadata tag `solution` (see `is_solution()` in [build_labs.py](build_labs.py)).
- Common pattern: a `# TODO` cell for students immediately followed by a `# @solution` cell with the answer.

### Common commands

Create a new lab (scaffolds `solutions/labNN_<slug>/labNN.ipynb` with a Colab badge derived from the git remote):
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

After building, both `labs/` and `solutions/` must be committed together — a lab isn't live for students until the rebuilt student notebook is pushed, not just the master.

## Notebook conventions

- Every answer cell must start with `# @solution` as its literal first line.
- Notebook outputs are stripped on commit via the `nbstripout` git filter (configured in local git config, `.venv/bin/python3 -m nbstripout`) — the repo stores only code/text, keeping diffs readable.
- Level 2+ labs that require installs should pin versions in a top install cell (e.g. `!pip install -q bertopic==0.16.0`) so notebooks don't break in future semesters.
- Every master notebook reminds students to use *File → Save a copy in Drive* since Colab runtimes are ephemeral.
- New labs need their row + Colab badge added to `README.md` in addition to the build step.

Full step-by-step workflow (creating vs. modifying labs, checklists) is in [WORKFLOW.md](WORKFLOW.md) — consult it for the exact sequence when doing lab authoring work.
