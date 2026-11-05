"""Generate a rights-safe fictional spreadsheet storyboard (no external images)."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
 ("毎月の集計、まだ手入力？","手入力で合計を計算","BEFORE"),
 ("SUM関数なら一瞬","=SUM(B2:B3)","ACTION"),
 ("合計が自動で更新","300","AFTER"),
]
def create_frames(folder):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i,(headline,detail,stage) in enumerate(SCENES):
        im=Image.new("RGB",(720,1280),"#081323"); d=ImageDraw.Draw(im)
        d.rounded_rectangle((34,65,686,160),radius=20,fill="#17314a")
        d.text((58,89),"AI 仕事術 / DEMO",font=ImageFont.truetype(BOLD,32),fill="#91e4ff")
        d.text((42,240),headline,font=ImageFont.truetype(BOLD,43),fill="white")
        d.rounded_rectangle((42,390,678,880),radius=24,fill="#f4f8fb")
        d.rectangle((42,390,678,455),fill="#d6e5ef")
        d.text((65,401),"架空のスプレッドシート",font=ImageFont.truetype(FONT,27),fill="#152b3b")
        for y in (520,615,710,805): d.line((65,y,655,y),fill="#b3c6d1",width=2)
        for x in (170,415): d.line((x,465,x,835),fill="#b3c6d1",width=2)
        for j,s in enumerate(("項目","売上A","売上B","合計")):
            d.text((75,477+j*94),s,font=ImageFont.truetype(FONT,26),fill="#223647")
        for j,s in enumerate(("金額","120","180","手計算中…" if i==0 else "300")):
            d.text((450,477+j*94),s,font=ImageFont.truetype(BOLD,27),fill="#223647")
        d.rounded_rectangle((42,915,678,1045),radius=18,fill="#183b54")
        d.text((70,945),detail,font=ImageFont.truetype(BOLD,37),fill="#b5f5e8")
        d.text((42,1090),stage,font=ImageFont.truetype(BOLD,29),fill="#8ddded")
        d.text((42,1150),"※ 架空データ / 社外公開未承認",font=ImageFont.truetype(FONT,22),fill="#b2c5d2")
        path=folder/f"scene{i}.png";im.save(path);paths.append(path)
    return paths

def render(folder, audio, output):
    folder=Path(folder); paths=create_frames(folder)
    playlist=folder/"concat.txt"
    playlist.write_text("".join(f"file '{p.resolve()}'\nduration 6\n" for p in paths)+f"file '{paths[-1].resolve()}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(playlist),"-i",str(audio),
      "-map","0:v","-map","1:a:0","-vf","fps=24,format=yuv420p","-t","18",
      "-c:v","libx264","-c:a","aac","-movflags","+faststart",str(output)],check=True)
if __name__=="__main__":
    import sys
    if len(sys.argv)!=4: raise SystemExit("usage: render_story.py WORKDIR APPROVED_AUDIO.mp4 OUTPUT.mp4")
    render(*sys.argv[1:])
