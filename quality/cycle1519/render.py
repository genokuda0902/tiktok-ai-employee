"""Review-only synthetic 3-scene renderer. Requires Pillow and ffmpeg. No speech; never publish."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
W,H,FPS,DURATION=720,1280,24,8
SCENES=[(0,2.5,"資料作成、まだ手作業？","最初に目的を一行で整理"),(2.5,5.2,"AIに条件を伝える","対象・形式・制約を明確に"),(5.2,8,"最後は人が確認","事実と個人情報をチェック")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def scene(t):
    return next((s for s in SCENES if s[0]<=t<s[1]),SCENES[-1])
def frame(t):
    im=Image.new("RGB",(W,H),(9,17,33));d=ImageDraw.Draw(im)
    head=ImageFont.truetype(FONT,43);sub=ImageFont.truetype(REG,29);small=ImageFont.truetype(REG,22)
    d.rounded_rectangle((35,95,685,1155),radius=32,fill=(21,35,59))
    d.text((70,145),"AI時短ラボ  /  REVIEW",font=small,fill=(100,212,223))
    d.text((70,215),"仕事を短くする3ステップ",font=ImageFont.truetype(FONT,35),fill="white")
    _,_,title,caption=scene(t)
    d.rounded_rectangle((70,325,650,825),radius=25,fill=(32,52,78))
    for i,(label,val) in enumerate([("目的",.88),("条件",.70),("確認",.94)]):
        y=380+i*125;d.text((105,y),label,font=sub,fill="white")
        d.rounded_rectangle((215,y+8,600,y+37),radius=14,fill=(53,73,94))
        progress=min(1,max(0,(t-i*1.3)/1.5))
        width=int(385*val*progress)
        if width>0:d.rounded_rectangle((215,y+8,215+width,y+37),radius=min(14,width//2),fill=(50,210,199))
    d.text((70,900),title,font=head,fill="white")
    d.text((70,975),caption,font=sub,fill=(209,225,236))
    d.rounded_rectangle((70,1080,650,1091),radius=5,fill=(56,74,93))
    d.rounded_rectangle((70,1080,70+int(580*t/DURATION),1091),radius=5,fill=(65,217,207))
    d.text((70,1180),"音声未生成 / 投稿禁止 / REVIEW ONLY",font=small,fill=(255,180,140))
    return im
def render(path):
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-an","-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p","-movflags","+faststart",str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close()
    if p.wait():raise RuntimeError("ffmpeg failed")
if __name__=="__main__":render(Path(__file__).parent/"cycle1519_REVIEW_ONLY.mp4")
