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

def plot_lcs_lengths(inmages_path: str, start_year: int, end_year: int):
    lcs_lengths = []

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            # compare w/ every other image IN THIS MONTHLY FOLDER, i.e. 
            # no comparison w/ images in other folders...
            dir = Path(f"{inmages_path}/{year}/{month}")
            if dir.exists():
                for file in dir.iterdir():
                    if file.is_file() and file.suffix == '.jpg':
                        image = cv2.imread(file)
                        image_str = pytesseract.image_to_string(image)
                        for other_file in dir.iterdir():
                            if other_file.is_file() and other_file.suffix == '.jpg' \
                                and file.name != other_file.name:
                                other_image = cv2.imread(other_file)
                                other_image_str = pytesseract.image_to_string(
                                                                other_image)
                                lcs_lengths.append(pylcs.lcs_string_length(image_str, 
                                                                           other_image_str))

    pyplot.boxplot(lcs_lengths)
    pyplot.title(f"{inmages_path}: longest commont substring lengths")
    pyplot.show()
