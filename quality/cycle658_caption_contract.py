"""Literal Japanese subtitle helper."""

def split_caption(text):
    mid = (len(text) + 1) // 2
    return text[:mid], text[mid:]
