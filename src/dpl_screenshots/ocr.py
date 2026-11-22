import random
from pathlib import Path

import cv2
import matplotlib.pyplot as pyplot
import pylcs
import pytesseract


def getimagetext(imagepath: str) -> str:
    img = cv2.imread(imagepath)
    return pytesseract.image_to_string(img)

def get_lcs_length(image0_text: str, image1_text: str) -> int:
    return pylcs.lcs_string_length(image0_text, image1_text)

def plot_lcs_lengths(images_path: str, start_year: int, end_year: int):

    sample_files: Path = []
    sample_file_pairs: str = []
    image_str_pairs: str = []
    lcs_lengths = []
    random.seed(42)

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            dir = Path(f"{images_path}/{year}/{month}")
            if dir.exists() and dir.is_dir():
                for file in dir.iterdir():
                    if file.is_file() and file.suffix == '.jpg' \
                        and random.random() <= 0.01:
                        sample_files.append(file)

    for file in sample_files:
        image = cv2.imread(file)
        image_str = pytesseract.image_to_string(image)
        for other_file in sample_files:
            if file.name != other_file.name:
                other_image = cv2.imread(other_file)
                other_image_str = pytesseract.image_to_string(other_image)
                lcs_lengths.append(pylcs.lcs_string_length(image_str, other_image_str))
                sample_file_pairs.append(f"{file} | {other_file}")
                image_str_pairs.append(f"{image_str} | {other_image_str}")

    pyplot.boxplot(lcs_lengths)
    pyplot.title(f"{images_path}: longest common substrings of random sample of files")
    pyplot.show()

    for i in range(0,5):
        print(sample_file_pairs[i])
        print(image_str_pairs[i])
