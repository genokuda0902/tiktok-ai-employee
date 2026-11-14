"""Synthetic review renderer; no private footage. NOT FOR PUBLICATION."""
from pathlib import Path
import subprocess, json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CAPTIONS=["合計を毎回、手で入力していませんか？","SUM関数で、合計を自動計算。","結果が正しいか、最後に確認。"]
def render(out=None,fps=24):
    out=Path(out) if out else ROOT/"review.mp4"
    out.parent.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype(FONT,22)
    cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pixel_format","rgb24","-video_size","540x960","-framerate",str(fps),"-i","-","-vf","scale=1080:1920,format=yuv420p","-c:v","libx264","-preset","ultrafast","-movflags","+faststart",str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for frame in range(12*fps):
        t=frame/fps; stage=min(2,int(t//4))
        im=Image.new("RGB",(540,960),"#101a2b");d=ImageDraw.Draw(im)
        d.rounded_rectangle((25,100,515,740),radius=22,fill="#f0f5f7")
        d.text((50,140),["課題：手計算","実演：SUM関数","結果：検算"][stage],font=font,fill="#16465c")
        for x in [65,185,315,475]: d.line((x,240,x,560),fill="#afc5cc",width=2)
        for y in [240,304,368,432,496,560]:d.line((65,y,475,y),fill="#afc5cc",width=2)
        for i,value in enumerate(["1,200","2,300","3,200"]):d.text((326,308+i*64),value,font=font,fill="#1c3547")
        if stage==1:
            chars=min(11,int((t-4)*5))
            d.text((70,590),"=SUM(B2:B4)"[:chars],font=font,fill="#087f71")
        elif stage==2:d.text((326,503),"6,700",font=font,fill="#087f71")
        cx=95 if stage==0 else (70+int(min(1,max(0,(t-4)/4))*365) if stage==1 else 335)
        cy=315 if stage==0 else 535
        d.polygon([(cx,cy),(cx+10,cy+25),(cx+15,cy+16),(cx+25,cy+12)],fill="#ef8e44")
        d.rounded_rectangle((25,772,515,875),radius=14,fill="#174658")
        d.text((39,803),CAPTIONS[stage],font=font,fill="white")
        d.rectangle((25,890,25+int(490*(frame+1)/(fps*12)),898),fill="#2bc4b5")
        d.text((26,918),"架空データ・音声なし・社内確認専用",font=ImageFont.truetype(FONT,16),fill="#ffca9e")
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait():raise RuntimeError("ffmpeg encoding failed")
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    return out
if __name__=="__main__":print(render())
