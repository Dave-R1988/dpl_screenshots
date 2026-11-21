import argparse
from collections.abc import Sequence

from . import ocr


def analyze_imagetexts(screenshots_path: str) -> None:
    ocr.plot_lcs_lengths(screenshots_path, 2024, 2026)


def analyze_imagehistograms(screenshots_path: str) -> None:
    raise NotImplementedError("analyze-imagehistograms is not implemented yet")


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

    args = parser.parse_args(argv)
    if args.command == "analyze-imagetexts":
        analyze_imagetexts(args.screenshots_path)
    elif args.command == "analyze-imagehistograms":
        analyze_imagehistograms(args.screenshots_path)


if __name__ == "__main__":
    main()