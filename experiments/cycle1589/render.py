"""Review-only synthetic spreadsheet demo; no private assets or automatic posting."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("集計に時間をかけない","手入力 → 関数で自動集計","毎日の数字をもっと見やすく"),("入力するのはデータだけ","=SUM(B2:B5)","合計は自動で更新される"),("確認してから共有","数式と元データをチェック","最後は人が確認する")]
def render():
    clips=[]
    for i,(headline,formula,subtitle) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),(9,19,37)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((35,115,685,1135),radius=34,fill=(22,38,60))
        d.rounded_rectangle((65,310,655,855),radius=24,fill=(242,246,252))
        d.text((60,170),f"0{i+1} / 03",font=ImageFont.truetype(BOLD,35),fill=(77,220,213))
        d.text((60,235),headline,font=ImageFont.truetype(BOLD,37),fill="white")
        for j,s in enumerate(["A         B          C","項目       数値        合計","月曜        12","火曜        18","水曜        20"]):
            d.text((93,340+j*85),s,font=ImageFont.truetype(FONT,30),fill=(26,45,70))
            d.line((83,395+j*85,637,395+j*85),fill=(195,208,221),width=2)
        d.rounded_rectangle((85,785,630,845),radius=12,fill=(25,117,132))
        d.text((100,793),formula,font=ImageFont.truetype(BOLD,26),fill="white")
        d.text((65,965),subtitle,font=ImageFont.truetype(FONT,30),fill="white")
        d.text((65,1070),"DEMO / REVIEW ONLY",font=ImageFont.truetype(FONT,23),fill=(130,160,180))
        png=ROOT/f"scene{i}.png"; clip=ROOT/f"scene{i}.mp4"; im.save(png)
        subprocess.run(["ffmpeg","-y","-loop","1","-framerate","24","-i",str(png),"-t","3","-vf","zoompan=z='min(zoom+0.0007,1.08)':d=1:s=720x1280:fps=24,format=yuv420p","-c:v","libx264","-preset","ultrafast","-r","24",str(clip)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        clips.append(clip)
    playlist=ROOT/"concat.txt"
    playlist.write_text("".join(f"file '{p}'\n" for p in clips))
    output=ROOT/"cycle1589_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(playlist),"-c","copy","-movflags","+faststart",str(output)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return output
if __name__=="__main__": print(render())
