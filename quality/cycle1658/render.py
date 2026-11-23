"""Three-scene, zero-cost review-only vertical demo; requires Pillow and FFmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
LINES=[
 ("毎日の集計、まだ手作業？","BEFORE","手入力・転記ミスに注意"),
 ("AIで表の形を整える","DEMO / AFTER","表形式で整理 → 確認"),
 ("確認してから活用する","CHECK","数値・個人情報を必ず確認")]
def draw(i):
    im=Image.new("RGB",(1080,1920),"#0b1424")
    d=ImageDraw.Draw(im)
    f=lambda size:ImageFont.truetype(FONT,size)
    d.rounded_rectangle((55,100,1025,1780),radius=40,fill="#15243a")
    for y,s,size,col in [(170,"AI × Excel 仕事術",48,"#54ded4"),(290,LINES[i][0],55,"white"),(390,LINES[i][1],44,"#f9c56a"),(1310,LINES[i][2],44,"#54ded4"),(1690,"REVIEW ONLY / 音声未生成・投稿禁止",32,"#ffb8b8")]:
        d.text((100,y),s,font=f(size),fill=col)
    d.rounded_rectangle((90,530,990,1190),radius=18,fill="#edf3f8")
    d.rectangle((90,530,990,610),fill="#276280")
    for j,s in enumerate(["商品","件数","金額"]):d.text((135+j*280,545),s,font=f(34),fill="white")
    for k,row in enumerate([("A商品","12","24,000"),("B商品","8","16,000"),("C商品","15","30,000")]):
        for j,s in enumerate(row):d.text((135+j*280,670+k*145),s,font=f(36),fill="#19314a")
    path=ROOT/f"scene{i}.png";im.save(path);return path
def main():
    ROOT.mkdir(exist_ok=True,parents=True)
    clips=[]
    for i in range(3):
        image=draw(i);clip=ROOT/f"clip{i}.mp4";clips.append(clip)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","24","-i",str(image),"-vf","zoompan=z='min(zoom+0.0003,1.04)':d=120:s=1080x1920:fps=24,format=yuv420p","-frames:v","120","-c:v","libx264","-preset","ultrafast","-crf","24","-an",str(clip)],check=True)
    playlist=ROOT/"concat.txt"
    playlist.write_text("".join(f"file '{x}'\\n" for x in clips))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(playlist),"-c","copy","-movflags","+faststart",str(ROOT/"cycle1658_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__":main()
