"""Review-only common scene layout checks; no publication approval."""
def validate_layout(boxes, width=1080, left=65, right=160):
    for x0,y0,x1,y1 in boxes:
        if not (left <= x0 < x1 <= width-right and 0 <= y0 < y1 <= 1920):
            raise ValueError("text outside review safe area")
def validate_timeline(bounds, count):
    if len(bounds)!=count+1 or bounds[0]!=0 or any(a>=b for a,b in zip(bounds,bounds[1:])):
        raise ValueError("invalid scene timeline")
