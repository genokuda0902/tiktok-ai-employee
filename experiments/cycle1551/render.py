"""Self-contained, review-only Japanese spreadsheet animation. Requires Pillow and ffmpeg."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
W,H,FPS,DUR=360,640,12,12
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def frame(t):
    im=Image.new("RGB",(W,H),"#0c1222"); d=ImageDraw.Draw(im)
    def txt(x,y,s,size=17,color="white",bold=False):
        d.text((x,y),s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)
    d.rounded_rectangle((15,20,345,95),radius=15,fill="#192943")
    txt(29,29,"Excel時短術",17,"#80eaff",True)
    txt(29,55,"合計を一瞬で出す方法",20,"white",True)
    d.rounded_rectangle((15,112,345,453),radius=15,fill="#f6f9fd")
    txt(30,130,"売上集計（架空の数値）",16,"#18263d",True)
    for j,(a,b) in enumerate([("商品","売上"),("A","120"),("B","230"),("C","150"),("合計","")]):
        y=171+j*46
        d.rectangle((30,y,330,y+44),fill=("#d8e9f9" if j==0 else "#ffffff" if j%2 else "#edf4fa"),outline="#d1dbe5")
        d.line((185,y,185,y+44),fill="#d1dbe5")
        txt(47,y+11,a,16,"#172638",j==0);txt(208,y+11,b,16,"#172638",j==0)
    if t<3:phase="① 手計算は時間がかかる";formula="120 + 230 + 150 = ?"
    elif t<6:
        phase="② 合計セルを選択";formula="セル B5 をクリック"
        d.rectangle((186,355,329,398),outline="#00a97f",width=3)
    elif t<9:
        phase="③ SUM関数を入力";s="=SUM(B2:B4)";formula=s[:min(len(s),int((t-6)*6)+1)]+"▏"
        d.rectangle((186,355,329,398),outline="#00a97f",width=3)
    else:
        phase="④ 合計が自動で完成";formula="500  ✓"
        d.rectangle((186,355,329,398),fill="#c9f7dc",outline="#00a97f",width=3)
        txt(208,366,"500",17,"#08754c",True)
    d.rounded_rectangle((15,473,345,581),radius=13,fill="#192943")
    txt(27,485,phase,19,"#80eaff",True);txt(27,527,formula,19,"white",True)
    d.rectangle((15,607,345,613),fill="#314157")
    d.rectangle((15,607,15+int(330*t/DUR),613),fill="#4cddc8")
    captions=["まず合計したい数値を確認","合計セルを選択します","SUM関数で範囲を指定","合計500が自動で出ます"]
    caption=captions[min(3,int(t//3))]
    d.rounded_rectangle((16,586,344,606),radius=5,fill="#030712")
    txt(25,588,caption,13,"#ffffff",True)
    txt(20,620,"REVIEW ONLY ・ 日本語音声なし",10,"#c3ccd9")
    return im
def render(path):
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-vf","scale=720:1280:flags=lanczos","-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DUR):p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close()
    if p.wait():raise RuntimeError("ffmpeg failed")
if __name__=="__main__":render(Path("cycle1551_REVIEW_ONLY.mp4"))
