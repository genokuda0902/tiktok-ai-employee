"""Photo-preserving layout component for 10-genre TikTok image slides.

cycle837: avoid destructive cover-cropping of people, screens, and text.
Review-only assets; this module does not upload, post, or access paid APIs.
"""
from PIL import Image

FRAME=(1080,1920)
PHOTO_BOX=(928,832)
GENRE_COLORS={
    "ai_work":"#4DE8DB","sales_business":"#FFC56B",
    "beauty":"#FF9DC9","romance":"#F9B6DD",
    "saving":"#F5D76E","career":"#8FB5FF",
    "wellness":"#9CE2B0","science":"#FFA980",
    "travel_food":"#C7A3FF","productivity":"#75DCEB"
}
ACTIONS=(
    "小さな仕事から試す","毎日やる作業を１つ選ぶ",
    "完成イメージを用意","目的・形式・条件を伝える",
    "誤りや漏れを確認","修正点を１つずつ伝える",
    "成功した指示を保存","明日も同じ型で試す"
)

def fit_contain(image: Image.Image, box=PHOTO_BOX) -> Image.Image:
    """Resize without cropping: entire source remains visible."""
    width,height=box
    if width<=0 or height<=0: raise ValueError("invalid photo box")
    scale=min(width/image.width,height/image.height)
    return image.resize(
        (max(1,round(image.width*scale)),max(1,round(image.height*scale))),
        Image.Resampling.LANCZOS
    )

def place_photo(image: Image.Image, canvas: Image.Image, top_left=(76,418)):
    """Paste photo centered in a fixed-size box, preserving all source pixels."""
    fitted=fit_contain(image)
    x=top_left[0]+(PHOTO_BOX[0]-fitted.width)//2
    y=top_left[1]+(PHOTO_BOX[1]-fitted.height)//2
    canvas.paste(fitted,(x,y))
    return (x,y,fitted.width,fitted.height)

def validate_genre(genre):
    if genre not in GENRE_COLORS: raise ValueError("unsupported genre")
    return GENRE_COLORS[genre]
