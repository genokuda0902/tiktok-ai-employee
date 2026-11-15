"""Reimplementation: self-contained review-only storyboard. Requires Pillow, ffmpeg and Noto CJK."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
P = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES = [
 ("AIで時短する前に","入力情報を確認","機密情報を入力しない"),
 ("依頼は具体的に","目的・条件・出力形式","3つの要素を整理"),
 ("結果は必ず確認","数字・固有名詞・根拠","人が最後にチェック"),
 ("今日から1つ試す","小さな作業から改善","保存して見返そう")
]
def render():
    for i,(a,b,c) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),"#0b1529")
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((45,120,675,1150),radius=36,fill="#182b46",outline="#3e6481",width=3)
        d.rectangle((45,120,675,135),fill="#00b7c7")
        d.text((75,195),f"0{i+1} / 04",font=ImageFont.truetype(BOLD,37),fill="#54dce1")
        d.text((75,350),a,font=ImageFont.truetype(BOLD,47),fill="white")
        d.rounded_rectangle((75,520,645,815),radius=22,fill="#244363")
        d.text((100,570),b,font=ImageFont.truetype(BOLD,35),fill="white")
        d.text((100,665),c,font=ImageFont.truetype(FONT,29),fill="#c2e5f3")
        d.text((80,1030),"REVIEW ONLY / 未承認",font=ImageFont.truetype(FONT,24),fill="#a8b7c9")
        im.save(P/f"s{i}.png")
    (P/"frames.txt").write_text("".join(f"file '{P/f's{i}.png'}'\\nduration 3\\n" for i in range(4))+f"file '{P/'s3.png'}'\\n")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(P/"frames.txt"),"-vf","fps=12,format=yuv420p","-c:v","libx264","-movflags","+faststart",str(P/"REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__":
    render()
