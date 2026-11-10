"""Review-only synthetic Excel clip. No external images or personal data."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
CAPTIONS=["合計を一瞬で出す方法","セルを選んでSUMを入力","範囲を指定して確定","合計は 45,000 円"]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def caption_at(t):
    return CAPTIONS[min(3,max(0,int(t//3)))]
def render(output="review.mp4",fps=15):
    w,h=720,1280
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(fps),"-i","-","-an","-c:v","libx264","-preset","ultrafast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",output]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    font=ImageFont.truetype(FONT,32)
    try:
        for frame in range(12*fps):
            t=frame/fps
            im=Image.new("RGB",(w,h),(11,18,34))
            d=ImageDraw.Draw(im)
            d.rounded_rectangle((40,160,680,850),radius=20,fill=(243,248,251))
            d.rectangle((40,160,680,240),fill=(31,112,85))
            d.text((65,180),"架空の売上データ",font=font,fill="white")
            for i,(day,amount) in enumerate([("月曜","10,000"),("火曜","12,000"),("水曜","8,000"),("木曜","15,000")]):
                y=260+i*105
                d.text((75,y),day,font=font,fill=(20,35,55))
                d.text((400,y),amount,font=font,fill=(20,35,55))
            d.text((70,720),["合計","=SUM(B2:B5)","=SUM(B2:B5)","45,000"][min(3,int(t//3))],font=font,fill=(22,84,65))
            d.rounded_rectangle((40,930,680,1100),radius=18,fill=(26,40,62))
            d.text((65,995),caption_at(t),font=font,fill="white")
            d.rectangle((40,1150,40+int(640*(frame+1)/(12*fps)),1162),fill=(64,212,165))
            proc.stdin.write(im.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError("ffmpeg failed")
    return Path(output)
if __name__=="__main__": print(render())
