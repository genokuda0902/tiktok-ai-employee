"""Cycle524 geometry checks for 10 genre synthetic review-only videos."""
GENRES = ("ai_work","beauty","relationship","money","sales","career","health","science","travel","products")
CAPTIONS = ((2.5,5.0,1400),(5.0,7.5,330),(7.5,10.0,1400),(10.0,12.5,1400),(12.5,15.0,1400),(15.0,17.5,1400))
def validate(genre, publication, privacy_checked, captions=CAPTIONS):
    if genre not in GENRES or publication != "NOT_APPROVED" or privacy_checked is not True:
        raise ValueError("review gate")
    last = 0.0
    for start,end,y in captions:
        if not (last<=start<end<=18 and 100<=y and y+116<=1536):
            raise ValueError("caption safe zone or timing")
        if start<7.5 and end>5 and y>=1000:
            raise ValueError("send button overlap")
        last=end
    return True
