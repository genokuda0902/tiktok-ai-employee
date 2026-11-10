"""Cycle1351: synthetic, rights-safe, review-only Excel explainer.
Requirements: Pillow, ffmpeg, Noto CJK fonts. No narration: do not approve for posting.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json
ROOT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
STEPS = [
 ("Excelの合計、まだ手計算？", "3秒でできる方法"),
 ("売上のセルを選択", "B2からB5まで"),
 ("=SUM(B2:B5)", "この式を入力するだけ"),
 ("合計  18,400円", "計算結果を必ず確認"),
]
def make_frame(i):
    im = Image.new("RGB", (720, 1280), "#0c1524")
    d = ImageDraw.Draw(im)
    def txt(x,y,s,size=36,color="white",bold=False):
        d.text((x,y),s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)
    txt(44,90,"EXCEL  /  仕事の時短",28,"#6fe2c4",True)
    txt(44,170,STEPS[i][0],43,"white",True)
    txt(44,240,STEPS[i][1],30,"#d5e3f0")
    d.rounded_rectangle((44,355,676,875),radius=20,fill="#f7fafc")
    d.rectangle((44,355,676,425),fill="#16825e")
    txt(67,367,"売上集計（架空データ）",28,"white",True)
    for k,(a,b) in enumerate([("月","売上"),("1月","3,200"),("2月","4,500"),("3月","5,100"),("4月","5,600")]):
        y=440+k*67
        d.line((65,y+58,655,y+58),fill="#cdd5dd",width=2)
        txt(80,y,a,26,"#263343")
        txt(400,y,b,26,"#263343")
    if i>=1:
        d.rounded_rectangle((385,500,575,770),radius=5,outline="#ef8b34",width=6)
    if i>=2:
        d.rounded_rectangle((72,795,647,852),radius=8,fill="#e4f2e9")
        txt(95,798,"=SUM(B2:B5)" if i==2 else "合計：18,400円",28,"#15643c",True)
    d.rounded_rectangle((44,960,676,1090),radius=16,fill="#17324a")
    txt(72,984,STEPS[i][1],32,"#ffffff",True)
    txt(44,1160,"※ 架空データ・レビュー専用",22,"#9db3c5")
    return im
def render():
    for i in range(4):
        make_frame(i).save(ROOT / f"frame{i}.png")
    concat=ROOT/"concat.txt"
    concat.write_text("".join(f"file '{ROOT}/frame{i}.png'\nduration 3\n" for i in range(4))+f"file '{ROOT}/frame3.png'\n")
    out=ROOT/"cycle1351_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-vf","fps=24,format=yuv420p","-t","12","-c:v","libx264","-preset","veryfast","-crf","23","-movflags","+faststart",str(out)],check=True)
    (ROOT/"manifest.json").write_text(json.dumps({"quality":"REVIEW_ONLY","posting_allowed":False,"japanese_narration":False,"speech_synced_captions":False,"rights":"synthetic assets only","duration_seconds":12},ensure_ascii=False,indent=2))
    return out
if __name__=="__main__":
    print(render())
