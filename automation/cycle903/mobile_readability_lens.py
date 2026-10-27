"""cycle903: mobile-readable focus cards for synthetic save UI.
No real data, paid services, publishing, or automatic approval.
"""
GENRES=("ai","beauty","romance","saving","sales","career","health","trivia","travel","product_comparison")
PHASES=((17.4,18.35),(18.35,19.3),(19.3,20.3))
ROI=((252,764,954,828),(159,852,960,1010),(740,1016,980,1095))
CAPTION_TOP=1450
CARD=(118,1110,962,1278)
TEXT=(
 ("01 / テンプレート名","週次報告テンプレ"),
 ("02 / 指示の内容","目的・条件・形式を確認"),
 ("03 / 保存操作","この画面はローカルデモ"),
)
RELEASE={"auto_post":False,"paid_services":False,"merge":False,"employee_approved":False}
def validate(genre="ai"):
    if genre not in GENRES: raise ValueError("unsupported genre")
    if any(RELEASE.values()): raise ValueError("review gate must remain closed")
    if CARD[3]>=CAPTION_TOP: raise ValueError("caption overlap")
    for x0,y0,x1,y1 in ROI:
        if not (0<=x0<x1<=1080 and 0<=y0<y1<CAPTION_TOP): raise ValueError("unsafe ROI")
    return True
def ffmpeg_filter(font,dirpath):
    validate()
    f=["drawbox=x=118:y=1110:w=844:h=168:color=0xF7FBFF@0.98:t=fill:enable='between(t,17.4,20.3)'",
       "drawbox=x=118:y=1110:w=844:h=5:color=0x10BFC2:t=fill:enable='between(t,17.4,20.3)'"]
    for i,((t0,t1),(x0,y0,x1,y1)) in enumerate(zip(PHASES,ROI)):
        enable=f"gte(t,{t0})*lt(t,{t1})"
        f.append(f"drawbox=x={x0}:y={y0}:w={x1-x0}:h={y1-y0}:color=0x10BFC2@0.26:t=fill:enable='{enable}'")
        f.append(f"drawbox=x={x0}:y={y0}:w={x1-x0}:h={y1-y0}:color=0x00C7BF:t=5:enable='{enable}'")
        for kind,size,y in (("title",30,1127),("detail",47,1180)):
            f.append(f"drawtext=fontfile={font}:textfile={dirpath}/stage_{i}_{kind}.txt:fontsize={size}:fontcolor=0x09284A:x=154:y={y}:enable='{enable}'")
    return ",".join(f)+",format=yuv420p"
