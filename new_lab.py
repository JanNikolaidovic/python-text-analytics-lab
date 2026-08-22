#!/usr/bin/env python3
"""Scaffold a new lab master notebook.

Creates  solutions/labNN_<slug>/labNN.ipynb  pre-filled with:
  * a correct "Open in Colab" badge (URL derived from your git remote)
  * a title/objectives block
  * one worked-example section and one exercise (with a # @solution cell)

Usage:
    python new_lab.py 02 data_structures "Data Structures & Control Flow"

Then edit the notebook in VS Code, and build the student version with:
    python build_labs.py solutions/lab02_data_structures/lab02.ipynb
"""
import re
import subprocess
import sys
from pathlib import Path

import nbformat as nbf
from nbformat.v4 import new_markdown_cell, new_notebook

BRANCH = "main"


def github_slug() -> str:
    """Return 'user/repo' from the git remote so the badge URL is correct."""
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "YOUR-GITHUB-USERNAME/python-text-analytics-lab"
    m = re.search(r"(?:github\.com[:/])([^/]+)/([^/]+?)(?:\.git)?$", url)
    return f"{m.group(1)}/{m.group(2)}" if m else "YOUR-GITHUB-USERNAME/python-text-analytics-lab"


def scaffold(num: str, slug: str, title: str) -> Path:
    num = num.zfill(2)
    folder = Path("solutions") / f"lab{num}_{slug}"
    master = folder / f"lab{num}.ipynb"
    if master.exists():
        sys.exit(f"Refusing to overwrite existing {master}")
    folder.mkdir(parents=True, exist_ok=True)

    student_rel = f"labs/lab{num}_{slug}/lab{num}_student.ipynb"
    badge_url = f"https://colab.research.google.com/github/{github_slug()}/blob/{BRANCH}/{student_rel}"

    cells = [
        new_markdown_cell(
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_url})"
        ),
        new_markdown_cell(f"# Lab {num} — {title}\n\n### Digital Skills and Business Decisioning Using Python"),
    ]

    nb = new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    }
    with open(master, "w") as f:
        nbf.write(nb, f)
    return master


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage: python new_lab.py <NN> <slug> "<Title>"')
        print('   e.g. python new_lab.py 02 data_structures "Data Structures & Control Flow"')
        sys.exit(1)
    path = scaffold(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:]))
    print(f"Created master: {path}")
    print("Next: edit it in VS Code, then run")
    print(f"  python build_labs.py {path}")
