from pathlib import Path
import hashlib
GENRES={"AI・仕事効率化":"#49E1DC","美容・身だしなみ":"#F5B0D5","恋愛・心理":"#F99CB4","お金・節約":"#F4D478","営業・ビジネス":"#86B9FF","転職・キャリア":"#B8ACF7","健康・生活改善":"#92DAB9","雑学・科学":"#8DDEEF","旅行・グルメ":"#FFB985","商品比較・暮らし":"#D1B9FA"}
WIDTH,HEIGHT,FPS=1080,1920,30
SCENE_START,SCENE_END=493,604
SAFE=(78,180,1000,1600)
DATA={"1月":120000,"2月":150000,"3月":200000,"4月":180000}
EXPECTED_CUE="三月二十万円、四月十八万円。"
def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()
def validate(m,source=None,storyboard=None):
    checks=[
        m.get("genre") in GENRES,
        set(m.get("supported_genres",[]))==set(GENRES),
        m.get("review_status")=="HUMAN_REVIEW",
        m.get("quality_approved") is False,
        m.get("post_policy")=="employee_manual_after_approval",
        m.get("media_rights")=="unverified_review_only",
        m.get("source_origin")=="user_provided_storyboard_review_only",
        m.get("claim")=="synthetic_comparison_only",
        m.get("synthetic_data") is True,
        m.get("narration_cue")==EXPECTED_CUE,
        m.get("data")==DATA,sum(DATA.values())==650000,
        DATA["4月"]-DATA["3月"]==-20000,
        source is None or sha256(source)==m.get("source_sha256"),
        storyboard is None or sha256(storyboard)==m.get("storyboard_sha256")
    ]
    if not all(checks): raise ValueError("review-only proof contract violated")
    return True
def safe_bbox(b):
    return SAFE[0]<=b[0] and b[2]<=SAFE[2] and SAFE[1]<=b[1] and b[3]<=SAFE[3]
def synthetic_smoke_frame(genre):
    from PIL import Image,ImageDraw,ImageFont
    if genre not in GENRES: raise ValueError("unknown genre")
    im=Image.new("RGB",(WIDTH,HEIGHT),(5,20,39))
    d=ImageDraw.Draw(im);accent=tuple(bytes.fromhex(GENRES[genre][1:]))
    d.rounded_rectangle((85,250,990,1540),radius=40,outline=accent,width=5)
    d.rounded_rectangle((120,550,520,1110),radius=30,fill=(20,56,75))
    d.rounded_rectangle((565,550,960,1110),radius=30,fill=(20,56,75))
    d.rounded_rectangle((175,810,450,1030),radius=20,fill=(61,184,230))
    d.rounded_rectangle((625,835,900,1030),radius=20,fill=accent)
    d.rounded_rectangle((120,1200,960,1430),radius=28,outline=accent,width=4)
    f=ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",55)
    for xy,s in [((140,650),"3月 200,000円"),((590,650),"4月 180,000円"),((180,1250),"前月比 −20,000円")]:
        if not safe_bbox(d.textbbox(xy,s,font=f)): raise ValueError("unsafe text")
        d.text(xy,s,font=f,fill=(245,251,255))
    return im
