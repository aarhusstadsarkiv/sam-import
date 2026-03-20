import argparse
from pathlib import Path

from .generate import handle_folder


def main():
    parser = argparse.ArgumentParser(
        prog="sam-import",
        description="Et script der generere metadata for en aflevering ud fra webformularen.",
    )
    parser.add_argument("path", help="Sti til mappen, der skal genereres metadata for.")
    args = parser.parse_args()

    path = Path(args.path)

    handle_folder(path)

    # Rename folder to [original name]_DONE
    if "_DONE" not in path.name:
        path.rename(path.parent / (path.name + "_DONE"))


if __name__ == "__main__":
    main()
