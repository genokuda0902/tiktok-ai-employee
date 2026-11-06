"""Review-only 1080p renderer. Reimplementation, not original v33. Requires Pillow and ffmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("01 / BEFORE","毎日の集計に時間がかかる","数字を探して、転記して、確認する"),("02 / ACTION","条件を決めて整理する","必要な項目だけをまとめる"),("03 / AFTER","確認しやすい一覧へ","最後は人がチェックする")]
def render(out=ROOT):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for i,(tag,title,sub) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),(9,18,35));d=ImageDraw.Draw(im)
        d.rounded_rectangle((60,220,1020,1570),radius=45,fill=(20,38,62))
        d.rectangle((60,220,78,1570),fill=(33,211,190))
        for y,s,size,color in [(310,tag,45,(80,230,205)),(530,title,61,"white"),(700,sub,35,(195,215,232)),(1660,"REVIEW ONLY / 投稿未承認",38,(250,185,90))]:
            d.text((110,y),s,font=ImageFont.truetype(FONT,size),fill=color)
        for j in range(3):
            d.rounded_rectangle((135,930+j*135,930,1010+j*135),radius=20,fill=(35,67,94))
            d.rounded_rectangle((155,950+j*135,155+(i+1)*210,990+j*135),radius=12,fill=(35,190,170))
        im.save(out/f"scene{i}.png")
    (out/"frames.txt").write_text("".join(f"file 'scene{i}.png'\nduration 5\n" for i in range(3))+"file 'scene2.png'\n")
    (out/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*5:02d},000 --> 00:00:{(i+1)*5:02d},000\n{scene[1]}\n\n" for i,scene in enumerate(SCENES)),encoding="utf-8")
    target=out/"cycle1262_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(out/"frames.txt"),"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-t","15","-r","30","-vf","format=yuv420p","-c:v","libx264","-preset","ultrafast","-crf","24","-c:a","aac","-b:a","96k","-movflags","+faststart",str(target)],check=True)
    return target
if __name__=="__main__": print(render())
