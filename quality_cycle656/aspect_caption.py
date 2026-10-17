from PIL import ImageOps, Image


def fit_artwork(image, size=(880, 630)):
    return ImageOps.contain(image, size, Image.Resampling.LANCZOS)


def split_caption(text):
    for symbol in ('、', '。'):
        pos = text.find(symbol)
        if 3 <= pos < len(text) - 3:
            return text[:pos+1], text[pos+1:]
    mid = len(text) // 2
    return text[:mid], text[mid:]
