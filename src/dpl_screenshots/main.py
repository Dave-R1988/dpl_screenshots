import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="dpl-screenshots",
        description="Screenshot utilities.",
        epilog="No screenshot commands are available yet.",
    )
    parser.parse_args(argv)
    parser.print_help()


if __name__ == "__main__":
    main()