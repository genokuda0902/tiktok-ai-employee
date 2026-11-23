"""Cycle1668: deterministic, fictional spreadsheet storyboard. Review-only."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
 ("01 / 課題","表の確認に時間がかかる","重複・空欄を手作業で探す"),
 ("02 / 操作","AIに確認条件を渡す","重複と空欄を一覧にして"),
 ("03 / 結果","確認箇所をすぐ把握","最後は人が内容を確認"),
]
def render(root=ROOT):
 root=Path(root);root.mkdir(parents=True,exist_ok=True)
 for i,(step,heading,sub) in enumerate(SCENES):
  im=Image.new("RGB",(1080,1920),"#0b1220");d=ImageDraw.Draw(im)
  font=lambda size,b=False:ImageFont.truetype(BOLD if b else FONT,size)
  d.rounded_rectangle((56,130,1024,1720),radius=42,fill="#152338")
  d.text((90,205),step,font=font(42),fill="#58d6cf")
  d.text((90,300),heading,font=font(58,True),fill="white")
  d.text((90,405),sub,font=font(38),fill="#c5d5e6")
  d.rounded_rectangle((92,570,988,1280),radius=25,fill="#eaf2f7")
  d.rectangle((92,570,988,650),fill="#305879")
  d.text((126,586),"サンプル表｜架空データ",font=font(32),fill="white")
  for j,status in enumerate(["入力済","確認待ち","入力済","重複候補","空欄","入力済"]):
   y=690+j*88;d.line((120,y+68,960,y+68),fill="#bdcbd5",width=2)
   d.text((140,y),f"No.{j+1:02d}",font=font(31),fill="#203b53")
   d.text((385,y),status,font=font(31),fill="#203b53")
   if j in (3,4):
    d.rounded_rectangle((755,y-4,935,y+56),radius=12,fill="#ffdf99" if i==0 else "#a8e8d1")
    d.text((770,y+4),"要確認" if i==0 else "抽出済",font=font(25),fill="#1b3643")
  d.rounded_rectangle((90,1370,990,1500),radius=20,fill="#254760")
  d.text((125,1405),["BEFORE  手作業で探す","DEMO  条件を指定","AFTER  候補を一覧化"][i],font=font(39,True),fill="white")
  d.text((90,1570),"※架空の操作イメージ／実際のExcel録画ではありません",font=font(25),fill="#b3c8d8")
  d.text((90,1790),"REVIEW ONLY  •  投稿未承認",font=font(31),fill="#a9b9c9")
  im.save(root/f"s{i}.png")
 playlist=root/"concat.txt"
 playlist.write_text("".join(f"file '{(root/f's{i}.png').resolve()}'\\nduration 4\\n".replace("\\n","\n") for i in range(3))+f"file '{(root/'s2.png').resolve()}'\n")
 out=root/"cycle1668_REVIEW_ONLY.mp4"
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(playlist),"-vf","fps=24,format=yuv420p","-t","12","-c:v","libx264","-preset","ultrafast","-movflags","+faststart",str(out)],check=True)
 return out
if __name__=="__main__":print(render())
