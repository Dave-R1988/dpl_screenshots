import cv2
import pylcs
import pytesseract


def getimagetext(imagepath: str):
    img = cv2.imread(imagepath)
    return pytesseract.image_to_string(img)

def get_lcs_length(image0_text: str, image1_text: str):
    return pylcs.lcs_string_length(image0_text, image1_text)