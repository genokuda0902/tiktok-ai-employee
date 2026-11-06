"""Review-only 1080p image-first renderer; public-safe synthetic graphics only."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

OUT = Path(__file__).resolve().parent
W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES = [
 ("AIの回答、\nそのまま使ってない？", "確認不足がミスにつながる", "01 / 課題"),
 ("まず「目的」と\n「条件」を明確に", "誰に・何を・どの形式で", "02 / 実践"),
 ("最後は人が\n事実をチェック", "出典・数字・個人情報を確認", "03 / 完成"),
]
CAPTIONS = ["AIの回答、そのまま使ってない？", "まず目的と条件を明確に。", "最後は人が事実をチェック。"]

def render():
    for i, (head, sub, tag) in enumerate(SCENES):
        im = Image.new("RGB", (W,H), (9,17,32))
        d = ImageDraw.Draw(im)
        for y in range(H):
            d.line((0,y,W,y), fill=(int(9+y/H*12),int(17+y/H*18),int(32+y/H*23)))
        d.rounded_rectangle((72,240,1008,1570), radius=54, fill=(20,37,58), outline=(46,91,112), width=3)
        d.rounded_rectangle((118,300,410,374), radius=25, fill=(29,132,146))
        d.text((146,315),tag,font=ImageFont.truetype(REG,34),fill="white")
        d.multiline_text((124,520),head,font=ImageFont.truetype(FONT,79),fill="white",spacing=38)
        d.rounded_rectangle((120,980,960,1215),radius=30,fill=(30,54,76))
        d.text((154,1040),sub,font=ImageFont.truetype(REG,42),fill=(211,238,241))
        for j in range(3):
            d.rounded_rectangle((125+j*290,1370,385+j*290,1390),radius=10,fill=(39,189,190) if j<=i else (66,86,101))
        d.text((120,1690),"AI WORKFLOW  /  REVIEW ONLY",font=ImageFont.truetype(REG,30),fill=(150,176,189))
        im.save(OUT/f"scene{i}.png")
    with (OUT/"concat.txt").open("w") as f:
        for i in range(3):
            f.write(f"file '{OUT}/scene{i}.png'\\nduration 5\\n".replace("\\n","\n"))
        f.write(f"file '{OUT}/scene2.png'\n")
    def ts(n): return f"00:00:{n:02d},000"
    (OUT/"captions.srt").write_text("".join(f"{i+1}\n{ts(i*5)} --> {ts((i+1)*5)}\n{t}\n\n" for i,t in enumerate(CAPTIONS)),encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(OUT/"concat.txt"),"-t","15","-vf","fps=24,format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","24","-movflags","+faststart",str(OUT/"cycle1263_REVIEW_ONLY.mp4")],check=True)

if __name__=="__main__": render()
