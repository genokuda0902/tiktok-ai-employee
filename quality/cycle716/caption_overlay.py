"""Reusable zero-cost Japanese caption overlay. REVIEW ONLY; not voice-synced.
Run: python quality/cycle716/caption_overlay.py input.mp4 output.mp4
Requires local ffmpeg with libass and Noto CJK font. No external services.
"""
import pathlib, subprocess, sys
LINES=[
("手作業とAI支援を比較","まず結果を見せる"),
("月別売上は架空データ","元データを確認"),
("AIに自然な言葉で指示","集計とグラフを依頼"),
("AIの答えは下書き","必ず数字を検算"),
("売上4か月をグラフ化","3月が最高20万円"),
("12＋15＋20＋18","合計65万円を確認"),
("AIが作った表も","最後は人が仕上げる"),
("元データ→AI→検算","保存してあとで試そう"),
]
BOX=(75,1575,930,140)
CANVAS=(1080,1920)
SAFE_BOTTOM=200
def validate():
    x,y,w,h=BOX
    assert x>0 and x+w<CANVAS[0] and y>CANVAS[1]//2
    assert y+h<=CANVAS[1]-SAFE_BOTTOM
    assert len(LINES)==8 and all(0<len(a)<=18 and 0<len(b)<=18 for a,b in LINES)
    assert not any("90%削減" in a+b or "一瞬で" in a+b for a,b in LINES)
def clock(t):
    return f"{t//3600}:{(t//60)%60:02}:{t%60:02}.00"
def write_ass(path):
    validate()
    header="""[Script Info]
Title: Cycle716 — review-only caption timing, NOT speech sync
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Noto Sans CJK JP,49,&H00FFFFFF,&H0000EFFF,&H00201510,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,5,90,90,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events=[]
    for i,(a,b) in enumerate(LINES):
        txt=r"{\an5\pos(540,1645)\fad(130,140)}"+a+r"\N{\c&H0000EFFF&}"+b
        events.append(f"Dialogue: 0,{clock(3*i)},{clock(3*(i+1))},Main,,0,0,0,,{txt}")
    pathlib.Path(path).write_text(header+"\n".join(events)+"\n",encoding="utf-8")
def render(src,dst):
    validate()
    src=pathlib.Path(src).resolve();dst=pathlib.Path(dst).resolve()
    if not src.is_file():raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    ass=dst.with_suffix(".ass");write_ass(ass)
    x,y,w,h=BOX
    vf=f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0x061527@1.0:t=fill,drawbox=x={x}:y={y}:w={w}:h={h}:color=0x33d5ef@0.8:t=3,ass={ass}"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-vf",vf,"-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r","30","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("usage: caption_overlay.py INPUT.mp4 OUTPUT.mp4")
    render(sys.argv[1],sys.argv[2])
