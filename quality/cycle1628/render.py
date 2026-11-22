"""Review-only 1080x1920 generator; no private/external assets. Requires Pillow and ffmpeg."""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
ROOT.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("入力がバラバラ…","同じ作業で毎回迷う"),("入力ルールを統一","項目を3つに絞る"),("チェックを自動化","抜け漏れを見える化"),("最後は人が確認","保存してあとで試そう")]
def render():
    clips=[]
    for i,(heading,sub) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),(8,16,32)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((52,180,1028,1725),radius=32,fill=(19,32,54),outline=(44,82,110),width=3)
        d.text((90,240),"AI WORKFLOW / DEMO",font=ImageFont.truetype(BOLD,38),fill=(82,220,218))
        d.text((90,395),heading,font=ImageFont.truetype(BOLD,70),fill="white")
        d.text((135,810),sub,font=ImageFont.truetype(FONT,48),fill=(193,210,224))
        d.rounded_rectangle((90,765,990,1470),radius=24,fill=(238,244,249))
        for j,label in enumerate(["目的を入力","条件を指定","内容を確認"]):
            y=945+j*140
            d.rounded_rectangle((135,y,940,y+95),radius=13,fill=(214,237,232) if j<i else (225,231,239))
            d.text((165,y+22),("✓ " if j<i else "□ ")+label,font=ImageFont.truetype(FONT,42),fill=(24,69,74))
        d.text((90,1580),f"0{i+1} / 04 • REVIEW ONLY",font=ImageFont.truetype(BOLD,32),fill=(100,205,205))
        frame=ROOT/f"frame_{i}.png"; clip=ROOT/f"clip_{i}.mp4"; im.save(frame)
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(frame),"-t","3","-c:v","libx264","-pix_fmt","yuv420p","-r","24",str(clip)],check=True)
        clips.append(clip)
    listing=ROOT/"concat.txt";listing.write_text("".join("file '"+str(p.resolve())+"'\n" for p in clips))
    out=ROOT/"cycle1628_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy","-movflags","+faststart",str(out)],check=True)
    (ROOT/"captions.json").write_text(json.dumps([{"start":i*3,"end":(i+1)*3,"text":s[0]} for i,s in enumerate(SCENES)],ensure_ascii=False,indent=2))
    return out
if __name__=="__main__": print(render())
