"""Caption safety geometry, independent of genre."""
SAFE=(54,192,1026,1536)
BOX=(55,1450,1025,1530)
def valid(box=BOX,safe=SAFE):
    return safe[0]<=box[0]<box[2]<=safe[2] and safe[1]<=box[1]<box[3]<=safe[3]
