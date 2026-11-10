"""Review-only synthetic 9s MP4 with original cue tone; NO Japanese narration."""
import argparse, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
SCENES=[("01 / 課題","音声がない動画は","完成ではありません"),("02 / 改善","字幕と音声を","同じ時間軸で管理"),("03 / 判定","日本語ナレーション","未実装・公開不可")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
WIDTH,HEIGHT,FPS,SECONDS=1080,1920,24,9
def scene_at(t): return min(2,int(t//3))
def draw_frame(t):
    im=Image.new("RGB",(WIDTH,HEIGHT),(10,18,34));d=ImageDraw.Draw(im);a=(62,206,202)
    d.rounded_rectangle((75,250,1005,1630),radius=48,fill=(24,39,62))
    d.rounded_rectangle((100,285,980,305),radius=10,fill=a)
    label,head,sub=SCENES[scene_at(t)]
    small=ImageFont.truetype(FONT,46);big=ImageFont.truetype(FONT,86)
    d.text((140,420),label,font=small,fill=a)
    d.text((140,690),head,font=big,fill="white")
    d.text((140,850),sub,font=big,fill="white")
    d.text((140,1270),"REVIEW ONLY  /  投稿禁止",font=small,fill=(250,190,110))
    d.text((140,1400),"音声：効果音のみ（日本語音声なし）",font=ImageFont.truetype(FONT,36),fill=(210,220,235))
    d.rounded_rectangle((140,1530,940,1545),radius=7,fill=(65,78,95))
    d.rounded_rectangle((140,1530,140+int(800*min(t/SECONDS,1)),1545),radius=7,fill=a)
    return im
def render(output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{WIDTH}x{HEIGHT}","-r",str(FPS),"-i","pipe:0","-f","lavfi","-i",f"sine=frequency=440:sample_rate=48000:duration={SECONDS}","-filter_complex","[1:a]volume=0.025,afade=t=in:st=0:d=0.2,afade=t=out:st=8.5:d=0.5[a]","-map","0:v","-map","[a]","-c:v","libx264","-preset","ultrafast","-crf","28","-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-t",str(SECONDS),"-movflags","+faststart",str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*SECONDS): p.stdin.write(draw_frame(i/FPS).tobytes())
    except BrokenPipeError: pass
    finally: p.stdin.close()
    if p.wait(): raise RuntimeError(f"ffmpeg failed: {p.returncode}")
    return output
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--output",default="cycle1365_REVIEW_ONLY.mp4")
    render(ap.parse_args().output)
