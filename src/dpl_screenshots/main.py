import argparse
from collections.abc import Sequence
from pathlib import Path

from . import duckdb_setup, ocr


def analyze_imagetexts(screenshots_path: str) -> None:
    ocr.plot_lcs_lengths(screenshots_path, 2024, 2026)


def analyze_imagehistograms(screenshots_path: str) -> None:
    raise NotImplementedError("analyze-imagehistograms is not implemented yet")

def db_setup(db_path: Path) -> None:
    duckdb_setup.duckdb_setup(db_path)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="dpl-screenshots",
        description="Image processing data pipeline commands.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    imagetexts_parser = subparsers.add_parser(
        "analyze-imagetexts",
        help="Analyze text in screenshots.",
    )
    imagetexts_parser.add_argument(
        "screenshots_path",
        help="Path to the screenshots.",
    )

    imagehistograms_parser = subparsers.add_parser(
        "analyze-imagehistograms",
        help="Analyze screenshot histograms.",
    )
    imagehistograms_parser.add_argument(
        "screenshots_path",
        help="Path to the screenshots.",
    )

    duckdb_setup = subparsers.add_parser(
        "db-setup",
        help="Set up db to store control and content data."
    )
    duckdb_setup.add_argument(
        "db_path",
        help="Directory where the database should be set up."
    )

    args = parser.parse_args(argv)
    if args.command == "analyze-imagetexts":
        analyze_imagetexts(args.screenshots_path)
    elif args.command == "analyze-imagehistograms":
        analyze_imagehistograms(args.screenshots_path)
    elif args.command == "db-setup":
        db_setup(Path(args.db_path))


if __name__ == "__main__":
    main()