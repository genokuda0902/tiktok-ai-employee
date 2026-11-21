"""Review-only 15-second Japanese captioned synthetic demo. No audio; never publish."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SCENES=[("集計、まだ手作業？","毎日の表計算をもっと速く"),("条件を入力","商品名と金額を整理"),("SUMIFで集計","条件に合う数字を合算"),("結果を確認","合計 128,000 円"),("最後に検算","元データとの一致を確認")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def render(out:Path):
    frames=out.parent/"frames";frames.mkdir(parents=True,exist_ok=True)
    for i in range(360):
        t=i/24;s=min(4,int(t//3));title,sub=SCENES[s];p=(t%3)/3
        im=Image.new("RGB",(720,1280),"#091325");d=ImageDraw.Draw(im)
        d.rounded_rectangle((32,80,688,1200),radius=36,fill="#15253b")
        d.text((64,130),"AI WORKFLOW / DEMO",font=ImageFont.truetype(REG,27),fill="#5fe3db")
        d.text((64,255),title,font=ImageFont.truetype(FONT,49),fill="white")
        d.text((64,335),sub,font=ImageFont.truetype(REG,29),fill="#c4d5e9")
        d.rounded_rectangle((64,470,656,970),radius=20,fill="#f0f5fa")
        d.rectangle((64,470,656,535),fill="#d7e6f2")
        for x,v in zip((88,315,515),("項目","数量","金額")):d.text((x,486),v,font=ImageFont.truetype(REG,24),fill="#1c344f")
        for j,(a,b,c) in enumerate((("商品A","4","32,000"),("商品B","2","18,000"),("商品A","12","96,000"))):
            y=560+j*100;d.line((82,y+68,635,y+68),fill="#c6d7e7",width=2)
            for x,v in zip((88,325,510),(a,b,c)):d.text((x,y),v,font=ImageFont.truetype(REG,23),fill="#1c344f")
        if s>=2:
            d.rounded_rectangle((85,885,635,945),radius=12,fill="#c2f1e8")
            d.text((100,891),"商品A 合計   128,000",font=ImageFont.truetype(FONT,27),fill="#0c4a42")
        d.rounded_rectangle((64,1070,656,1090),radius=10,fill="#314760")
        d.rounded_rectangle((64,1070,64+int(592*(s+p)/5),1090),radius=10,fill="#5fe3db")
        d.text((64,1120),f"STEP {s+1} / 5 • REVIEW ONLY",font=ImageFont.truetype(REG,22),fill="#d4e3f4")
        im.save(frames/f"{i:04}.png")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","24","-i",str(frames/"%04d.png"),"-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
if __name__=="__main__":render(Path("cycle1609_REVIEW_ONLY.mp4"))
