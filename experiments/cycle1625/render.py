"""Cycle1625: original-graphics, no-private-assets review-only renderer."""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
W,H,FPS=720,1280,12
SCENES=[("毎日の作業、","まだ手入力ですか？","入力ミスを減らす3ステップ"),("STEP 01","目的を1行で伝える","例：顧客リストを整理"),("STEP 02","出力形式を指定する","例：表で3列にまとめる"),("STEP 03","人が内容を確認","個人情報は入力しない")]
def render(out):
    fonts="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    bold="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    frames=ROOT/"frames";frames.mkdir(exist_ok=True)
    for n in range(12*FPS):
        t=n/FPS;i=min(3,int(t//3));p=(t-i*3)/3
        im=Image.new("RGB",(W,H),(9,17,32));d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,125,680,1130),radius=38,fill=(20,35,54),outline=(50,104,128),width=3)
        d.rounded_rectangle((75,190,645,610),radius=28,fill=(13,25,40))
        d.text((76,80),"AI / WORKFLOW",font=ImageFont.truetype(bold,28),fill=(84,221,210))
        a,b,c=SCENES[i]
        d.text((95,280),a,font=ImageFont.truetype(bold,48),fill=(84,221,210))
        d.text((95,375),b,font=ImageFont.truetype(bold,43),fill="white")
        d.text((95,680),c,font=ImageFont.truetype(fonts,30),fill=(222,231,239))
        d.rounded_rectangle((90,805,630,870),radius=20,fill=(31,54,75))
        if p>0.03:d.rectangle((90,805,90+int(540*p),870),fill=(52,180,177))
        d.text((100,980),"保存して、あとで試す",font=ImageFont.truetype(fonts,30),fill=(240,243,248))
        d.text((90,1170),f"{i+1:02d} / 04",font=ImageFont.truetype(fonts,30),fill=(132,164,185))
        im.save(frames/f"{n:04}.png")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),"-i",str(frames/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","25","-movflags","+faststart",str(out)],check=True)
    (ROOT/"captions.json").write_text(json.dumps([{"start":i*3,"end":(i+1)*3,"text":" ".join(s)} for i,s in enumerate(SCENES)],ensure_ascii=False,indent=2))
    (ROOT/"qa.json").write_text(json.dumps({"posting_allowed":False,"status":"PUBLICATION_NOT_APPROVED","narration_japanese":False,"speech_synced_captions":False,"employee_approved":False},indent=2))
if __name__=="__main__":render(ROOT/"cycle1625_REVIEW_ONLY.mp4")
