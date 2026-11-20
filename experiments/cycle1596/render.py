"""Public-safe six-scene review-only video. Requires Pillow and ffmpeg."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
O=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("01 / 課題","毎日の集計、まだ手入力？","作業の流れを見直そう"),("02 / 入力","数値を一度だけ入力","架空のサンプルデータ"),("03 / 計算","合計を自動で計算","120 + 180 + 200 = 500"),("04 / 確認","結果を人が確認","誤入力がないかチェック"),("05 / 比較","入力 → 集計 → 確認","工程を分けて考える"),("06 / まとめ","まずは小さく自動化","実データ・実績ではありません")]
def render():
 f=ImageFont.truetype(FONT,45); small=ImageFont.truetype(FONT,29)
 for i,(a,b,c) in enumerate(SCENES):
  im=Image.new("RGB",(720,1280),"#0a1222"); d=ImageDraw.Draw(im)
  d.rounded_rectangle((45,160,675,1080),radius=28,fill="#18273c")
  d.rectangle((45,160,675,171),fill="#49d5c1")
  d.text((80,240),a,font=small,fill="#49d5c1")
  d.multiline_text((80,410),b,font=f,fill="white",spacing=12)
  d.text((80,780),c,font=small,fill="#cbd5e1")
  d.text((80,1150),"REVIEW ONLY  |  生成サンプル",font=small,fill="#94a3b8")
  im.save(O/f"scene{i}.png")
 with (O/"concat.txt").open("w") as out:
  for i in range(6):out.write(f"file 'scene{i}.png'\nduration 2\n")
  out.write("file 'scene5.png'\n")
 subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(O/"concat.txt"),"-vf","fps=24,format=yuv420p","-c:v","libx264","-movflags","+faststart",str(O/"cycle1596_REVIEW_ONLY.mp4")],check=True)
if __name__=="__main__":render()
