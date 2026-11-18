import argparse
from collections.abc import Sequence

from .ocr import get_lcs_length, getimagetext


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="dpl-screenshots",
        description="Extract text from an image.",
    )
    parser.add_argument("image_path0", help="Path to the first image to read.")
    parser.add_argument("image_path1", help="Path to the second image to read.")
    args = parser.parse_args(argv)
    img_text0 = getimagetext(args.image_path0)
    img_text1 = getimagetext(args.image_path1)
    print(img_text0)
    print(img_text1)
    print(get_lcs_length(img_text0, img_text1))


if __name__ == "__main__":
    main()