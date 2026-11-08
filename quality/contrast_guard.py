"""Reusable no-cost slide contrast and safe-area guard."""
def luminance(rgb):
    c=[x/255 for x in rgb]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]

def contrast(fg,bg):
    a,b=sorted((luminance(fg),luminance(bg)),reverse=True)
    return (a+0.05)/(b+0.05)

def validate_slide(foreground,background,text_bottom,limit=1450,min_contrast=7):
    return contrast(foreground,background)>=min_contrast and text_bottom<limit
