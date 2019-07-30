import pytesseract
from PIL import Image


def tran2text(url):
    if str(url).endswith("jpg") or str(url).endswith("png") or str(url).endswith("bmp"):
        text = pytesseract.image_to_string(Image.open(str(url)), lang='chi_sim')
        return text
    else:
        return None


if __name__ == '__main__':
    text = tran2text("1.jpg")
    if text is not None:
        print(text)
