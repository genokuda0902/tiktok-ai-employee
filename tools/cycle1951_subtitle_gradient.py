"""Cycle1951: reusable smooth subtitle gradient overlay for vertical videos."""
from PIL import Image

def create_overlay(path, width=1080, height=1920, start_y=1260, max_alpha=27):
    assert 0 <= start_y < height
    assert 0 <= max_alpha <= 255
    im = Image.new("RGBA", (width, height), (0,0,0,0))
    for y in range(start_y, height):
        t = (y-start_y)/(height-start_y)
        a = round(max_alpha * t*t*(3-2*t))
        im.paste((0,0,0,a), (0,y,width,y+1))
    im.save(path)

if __name__ == "__main__":
    create_overlay("gradient_overlay.png")
