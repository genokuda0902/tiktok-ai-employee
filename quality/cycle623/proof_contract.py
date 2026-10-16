"""Reusable synthetic 10-genre visual proof checks, cycle623."""
GENRES = ("ai_work","beauty","relationships","money","sales_business",
          "career","health_lifestyle","science_trivia","travel_food","product_lifestyle")
START,END,FPS = 10.5,16.5,30
SAFE_BOUNDS=(52,76,1032,1780)

class Proof:
    def __init__(self,genre="ai_work",values=(120,150,200,250),rights="SYNTHETIC_REVIEW_ONLY",
                 publication="NOT_APPROVED",auto_post=False,japanese_narration="ABSENT",
                 actual_excel_recording=False):
        self.genre=genre
        self.values=values
        self.rights=rights
        self.publication=publication
        self.auto_post=auto_post
        self.japanese_narration=japanese_narration
        self.actual_excel_recording=actual_excel_recording
    def validate(self):
        if self.genre not in GENRES: raise ValueError("Unknown genre")
        if len(self.values)!=4 or any(type(x) is not int or not 0<=x<=9999 for x in self.values):
            raise ValueError("Four integers required")
        if self.rights!="SYNTHETIC_REVIEW_ONLY" or self.publication!="NOT_APPROVED" or self.auto_post:
            raise ValueError("Approval gate")
        if self.japanese_narration!="ABSENT" or self.actual_excel_recording:
            raise ValueError("Unverified evidence")
        return {"values":list(self.values),"sum":sum(self.values),"formula":"=SUM(B2:B5)",
                "genre":self.genre,"narration":"ABSENT","caption_voice_sync":"NOT_VERIFIED",
                "publication":"NOT_APPROVED","auto_post":False}

def scene_at(second):
    if not START<=second<END:raise ValueError("Outside scene")
    return "range_selection" if second<12.7 else "formula_and_total" if second<14.5 else "four_bar_chart"

def in_safe_area(box):
    a,b,c,d=SAFE_BOUNDS
    x1,y1,x2,y2=box
    return a<=x1<x2<=c and b<=y1<y2<=d
