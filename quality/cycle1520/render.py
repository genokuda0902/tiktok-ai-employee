"""Review-only UI demo: staged spreadsheet formula/result. No narration; never publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
STAGES=("① 手入力の集計を確認","② SUM関数を入力","③ 合計640を自動計算","④ 結果を確認して保存")

def stage_at(seconds):
    return min(3,max(0,int(seconds//2)))

def render():
    font=lambda n: ImageFont.truetype(FONT,n)
    for i in range(120):
        t=i/15
        im=Image.new("RGB",(720,1280),"#091323")
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((35,95,685,1120),radius=32,fill="#16263c")
        d.text((65,135),"Excel作業、まだ手入力？",font=font(38),fill="white")
        d.text((65,215),"架空データで操作を実演",font=font(24),fill="#a8c5d9")
        d.rounded_rectangle((65,310,655,805),radius=15,fill="#f3f7f9")
        for x in (65,240,415,655):
            d.line((x,310,x,805),fill="#ccd9de",width=2)
        for y in range(310,806,70):
            d.line((65,y,655,y),fill="#ccd9de",width=2)
        d.rectangle((65,310,655,380),fill="#dce9ee")
        for x,s in ((100,"項目"),(270,"金額"),(455,"集計")):
            d.text((x,327),s,font=font(24),fill="#152838")
        for j,(s,v) in enumerate((("A",120),("B",180),("C",250),("D",90))):
            y=400+j*70
            d.text((100,y),s,font=font(25),fill="#23384a")
            d.text((270,y),str(v),font=font(25),fill="#23384a")
        if t>=2:
            d.rounded_rectangle((415,388,648,455),radius=8,fill="#fff0b3",outline="#e4a624",width=4)
            d.text((424,405),"=SUM(B2:B5)",font=font(19),fill="#263848")
        if t>=4:
            d.rounded_rectangle((415,462,648,528),radius=8,fill="#c7f5d5",outline="#2b9d61",width=4)
            d.text((455,477),"640",font=font(29),fill="#155b36")
        d.rounded_rectangle((65,865,655,990),radius=16,fill="#147b8c")
        d.text((90,890),STAGES[stage_at(t)],font=font(29),fill="white")
        d.text((65,1050),"REVIEW ONLY  /  音声未生成",font=font(22),fill="#f8c1aa")
        d.text((65,1170),"※架空データ・投稿未承認",font=font(21),fill="#b5c6d2")
        im.save(ROOT/f"f{i:03d}.png")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","15","-i",str(ROOT/"f%03d.png"),"-r","30","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(ROOT/"cycle1520_REVIEW_ONLY.mp4")],check=True)
    for p in ROOT.glob("f???.png"): p.unlink()

if __name__=="__main__": render()
