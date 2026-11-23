"""Four-step fictional spreadsheet storyboard, review-only. No narration is claimed."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[
("01 / 課題","重複チェック、まだ目視？","同じ番号が複数行にある例","BEFORE：確認候補が埋もれる"),
("02 / 指示","条件を具体的に伝える","「重複・空欄を一覧にして」","INPUT：チェック条件を指定"),
("03 / 結果","候補だけ色分け表示","重複2件・空欄1件（架空）","AFTER：確認対象が見える"),
("04 / 注意","最後は人が確認する","AIの判定は必ず検証","確認後に使う")]
def render():
    for i,(label,heading,sub,footer) in enumerate(SCENES):
        im=Image.new("RGB",(1080,1920),"#0a1222");d=ImageDraw.Draw(im)
        ft=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
        d.rounded_rectangle((58,125,1022,1730),radius=35,fill="#14243b")
        d.text((100,190),label,font=ft(42),fill="#57d8d1")
        d.text((100,290),heading,font=ft(53,True),fill="white")
        d.text((100,390),sub,font=ft(34),fill="#d5e2ed")
        d.rounded_rectangle((95,565,985,1290),radius=20,fill="#f1f6f9")
        d.rectangle((95,565,985,648),fill="#305b7d")
        d.text((130,587),"架空のサンプル表｜個人情報なし",font=ft(30),fill="white")
        for j,v in enumerate(["A-001","B-002","C-003","B-002","（空欄）","D-004"]):
            y=690+j*90
            d.line((120,y+70,960,y+70),fill="#c8d4dc",width=2)
            d.text((140,y),f"{j+1:02d}",font=ft(33),fill="#27455b")
            d.text((330,y),v,font=ft(33),fill="#27455b")
            if i>=2 and j in (1,3,4):
                d.rounded_rectangle((685,y-5,942,y+60),radius=10,fill="#ffd4a4" if j==4 else "#b9edd8")
                d.text((705,y+6),"空欄" if j==4 else "重複候補",font=ft(27),fill="#23445a")
            elif i==1 and j==3:
                d.rounded_rectangle((685,y-5,942,y+60),radius=10,fill="#dbe9fa")
                d.text((705,y+6),"検索中…",font=ft(27),fill="#23445a")
        d.rounded_rectangle((100,1380,980,1510),radius=20,fill="#284d68")
        d.text((135,1417),footer,font=ft(34,True),fill="white")
        d.text((100,1580),"※操作説明用の架空デモ／実際のExcel録画ではありません",font=ft(23),fill="#b7cad9")
        d.text((100,1800),"REVIEW ONLY｜日本語音声なし｜投稿禁止",font=ft(28),fill="#ffcfaa")
        im.save(ROOT/f"scene{i}.png")
    clips=[]
    for i in range(len(SCENES)):
        p=ROOT/f"clip{i}.mp4";clips.append(p)
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","24","-i",str(ROOT/f"scene{i}.png"),"-t","3.5","-vf","scale=1080:1920,format=yuv420p","-c:v","libx264","-preset","ultrafast","-an",str(p)],check=True)
    lst=ROOT/"concat.txt";lst.write_text("".join(f"file '{p}'\n" for p in clips))
    out=ROOT/"cycle1669_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy","-movflags","+faststart",str(out)],check=True)
    return out
if __name__=="__main__":print(render())
