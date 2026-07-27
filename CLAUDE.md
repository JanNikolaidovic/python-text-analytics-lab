# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Course materials (Jupyter notebooks) for the Python Text Analytics Lab, University of Piraeus, Department of Economics. Students run the notebooks in Google Colab.

## Setup

```bash
source .venv/bin/activate
```

`.venv` already contains the dependencies (nbformat, nbstripout, jupyter, etc.). There is no requirements.txt/pyproject.toml — the venv is the source of truth.

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
