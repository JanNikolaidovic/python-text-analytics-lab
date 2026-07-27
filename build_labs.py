"""Build the student notebook from a master notebook.

Masters live under  solutions/<lab>/labNN.ipynb  and double as the answer key
(they contain the # @solution cells). This script generates the student-facing
notebook, with answers stripped, under  labs/<lab>/labNN_student.ipynb.

A cell counts as a SOLUTION cell if either:
  * its first non-empty line is exactly  # @solution   (recommended), or
  * it carries the notebook metadata tag 'solution'.

Usage:
    python build_labs.py solutions/lab01_setup_basics/lab01.ipynb [more masters...]
"""
import sys
from pathlib import Path
import nbformat


def is_solution(cell) -> bool:
    if cell.cell_type != "code":
        return False
    if "solution" in cell.get("metadata", {}).get("tags", []):
        return True
    first = next((ln.strip() for ln in cell.source.splitlines() if ln.strip()), "")
    return first == "# @solution"


def student_path_for(master: Path) -> Path:
    parts = list(master.parts)
    if parts and parts[0] == "solutions":       # solutions/<lab>/  ->  labs/<lab>/
        parts[0] = "labs"
    else:                                        # fallback if run from elsewhere
        parts = ["labs", master.parent.name, master.name]
    return Path(*parts[:-1]) / f"{master.stem}_student.ipynb"


def build(master_path: str) -> None:
    master = Path(master_path)
    nb = nbformat.read(master, as_version=4)
    removed = sum(is_solution(c) for c in nb.cells)
    nb.cells = [c for c in nb.cells if not is_solution(c)]

    student_path = student_path_for(master)
    student_path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, student_path)
    print(f"  answer key : {master}")
    print(f"  student -> : {student_path}   ({removed} solution cell(s) stripped)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_labs.py solutions/<lab>/labNN.ipynb [more...]")
        sys.exit(1)
    for p in sys.argv[1:]:
        print(f"Building from {p}:")
        build(p)
