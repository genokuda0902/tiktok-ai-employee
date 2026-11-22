"""Review-only 5-scene video generator. Requires Pillow, ffmpeg and Japanese Noto fonts.
Usage: python tools/cycle1643_review.py --out /tmp/cycle1643.mp4
This reimplementation is NOT the original v33 engine.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCENES = [
 ("入力のムダを減らす", "毎回、同じ情報を打っていませんか？"),
 ("BEFORE", "氏名 / 日付 / 金額\n毎回ゼロから入力"),
 ("AFTER", "入力項目をテンプレート化\n確認だけ人が担当"),
 ("3つのチェック", "① 入力漏れ\n② 表記ゆれ\n③ 個人情報"),
 ("小さく始める", "まず1つの作業から\n結果は必ず人が確認"),
]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def render(out):
    out=Path(out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for i,(title,body) in enumerate(SCENES):
            im=Image.new("RGB",(1080,1920),"#0a1223")
            d=ImageDraw.Draw(im)
            d.rounded_rectangle((65,170,1015,1640),radius=46,fill="#14243b",outline="#2b4e69",width=3)
            d.text((120,460),title,font=ImageFont.truetype(BOLD,77),fill="white")
            for j,line in enumerate(body.split("\n")):
                d.text((120,740+j*125),line,font=ImageFont.truetype(FONT,48),fill="#d9edf5")
            d.text((120,1350),f"{i+1:02d}/05  REVIEW ONLY",font=ImageFont.truetype(BOLD,40),fill="#80e1e8")
            d.text((110,1730),"※ 模擬データ・未承認 / 自動投稿禁止",font=ImageFont.truetype(FONT,31),fill="#b3c1ce")
            im.save(tmp/f"scene{i}.png")
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-y"]
        for i in range(5):
            cmd+=["-loop","1","-framerate","24","-t","4","-i",str(tmp/f"scene{i}.png")]
        filters="".join(f"[{i}:v]scale=1080:1920,format=yuv420p,trim=duration=4,setpts=PTS-STARTPTS[v{i}];" for i in range(5))
        filters+="".join(f"[v{i}]" for i in range(5))+"concat=n=5:v=1:a=0[v]"
        cmd+=["-filter_complex",filters,"-map","[v]","-c:v","libx264","-preset","ultrafast","-crf","27","-pix_fmt","yuv420p","-movflags","+faststart",str(out)]
        subprocess.run(cmd,check=True)
    return out

def verify(path):
    import json
    p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height","-show_entries","format=duration","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    assert any(s.get("codec_type")=="video" and s.get("width")==1080 and s.get("height")==1920 for s in data["streams"])
    assert 19.9<float(data["format"]["duration"])<20.1
    assert not any(s.get("codec_type")=="audio" for s in data["streams"]), "Unexpected audio"
    subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],check=True)
    return {"video_decode":True,"japanese_narration":False,"speech_synced_captions":False,"posting_allowed":False}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    args=p.parse_args()
    print(verify(render(args.out)))
