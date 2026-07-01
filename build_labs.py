"""Build student + solution notebooks from a master notebook.

A cell counts as a SOLUTION cell if either:
  * its first non-empty line is exactly  # @solution   (recommended), or
  * it carries the notebook metadata tag 'solution'.

Usage:
    python build_labs.py labs/lab01_setup_basics/lab01.ipynb [more masters...]

For each master `labNN.ipynb` it writes, in the same folder:
    labNN_student.ipynb     <- solution cells removed
    labNN_solutions.ipynb   <- full version (all cells kept)
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


def build(master_path: str) -> None:
    master = Path(master_path)
    nb = nbformat.read(master, as_version=4)

    student = nbformat.read(master, as_version=4)
    student.cells = [c for c in student.cells if not is_solution(c)]

    stem = master.stem
    student_path = master.with_name(f"{stem}_student.ipynb")
    solutions_path = master.with_name(f"{stem}_solutions.ipynb")

    nbformat.write(student, student_path)
    nbformat.write(nb, solutions_path)
    n_removed = len(nb.cells) - len(student.cells)
    print(f"  {student_path.name}   (student, {n_removed} solution cell(s) removed)")
    print(f"  {solutions_path.name} (solutions, full)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_labs.py <master.ipynb> [<master2.ipynb> ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        print(f"Building from {path}:")
        build(path)
