"""Standalone synthetic story renderer. Review only; no approved voice or synced captions."""
from pathlib import Path
import argparse, subprocess
from PIL import Image, ImageDraw, ImageFont
SCENES=[("BEFORE","毎日の集計に時間がかかる","120 + 180 = ?"),("ACTION","合計の式を入力する","=SUM(B2:B3)"),("AFTER","合計が自動で表示される","300")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def render(output):
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 folder=output.parent/"frames";folder.mkdir(exist_ok=True)
 for i,(tag,caption,content) in enumerate(SCENES):
  im=Image.new("RGB",(720,1280),"#0a1223");d=ImageDraw.Draw(im)
  d.rounded_rectangle((42,160,678,1010),radius=35,fill="#16233a",outline="#3b536e",width=3)
  d.text((62,75),"AI WORKFLOW / DEMO",font=ImageFont.truetype(BOLD,29),fill="#78e6e0")
  d.text((65,210),tag,font=ImageFont.truetype(BOLD,65),fill="white")
  d.rounded_rectangle((80,350,640,680),radius=18,fill="#edf3fa")
  for y,t in [(395,"B列    数値"),(500,"B2       120"),(565,"B3       180")]:d.text((115,y),t,font=ImageFont.truetype(FONT,32),fill="#263448")
  d.line((100,475,620,475),fill="#b5c6d8",width=3)
  d.text((80,745),content,font=ImageFont.truetype(BOLD,48),fill="#66eee0")
  d.rounded_rectangle((35,1040,685,1170),radius=22,fill="#f2f5fa")
  d.text((60,1070),caption,font=ImageFont.truetype(BOLD,31),fill="#142238")
  d.text((48,1210),"架空データ / REVIEW ONLY / 投稿禁止",font=ImageFont.truetype(FONT,20),fill="#b2c1d4")
  im.save(folder/f"{i:02}.png")
 manifest=folder/"concat.txt"
 manifest.write_text("".join(f"file '{(folder/f'{i:02}.png').resolve()}'\\nduration 5\\n" for i in range(3)).replace("\\n","\n")+f"file '{(folder/'02.png').resolve()}'\n")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(manifest),"-vf","fps=24,format=yuv420p","-t","15","-an","-c:v","libx264","-movflags","+faststart",str(output)],check=True)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--output",required=True);render(p.parse_args().output)
