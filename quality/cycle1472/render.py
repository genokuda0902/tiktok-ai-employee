"""Review-only fictional spreadsheet motion demo. No private assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SCENES=[("毎日の集計、まだ手作業？","同じ数字を何度も転記していませんか"),("BEFORE｜手入力","架空の売上表を毎日まとめる"),("AFTER｜AIで整理","項目を指定して表にまとめる"),("最後は人が確認","数字と個人情報をチェックして保存")]
def render():
    frames=ROOT/"frames"; frames.mkdir(exist_ok=True)
    for i in range(144):
        s=i//36; t=(i%36)/36
        im=Image.new("RGB",(720,1280),"#081421"); d=ImageDraw.Draw(im)
        big=ImageFont.truetype(BOLD,45); med=ImageFont.truetype(FONT,28); small=ImageFont.truetype(FONT,22)
        d.rounded_rectangle((42,68,678,150),radius=24,fill="#132d42")
        d.text((68,89),"AI WORKFLOW / REVIEW ONLY",font=small,fill="#65e0df")
        d.text((48,202),SCENES[s][0],font=big,fill="white")
        d.rounded_rectangle((40,310,680,920),radius=25,fill="#f0f5f8")
        d.rounded_rectangle((58,335,662,390),radius=12,fill="#dbe7ed")
        d.text((82,348),"DEMO SHEET · 架空データ",font=small,fill="#173549")
        for col,h in enumerate(["商品","月曜","火曜","水曜"]):
            d.text((77+col*145,440),h,font=small,fill="#24495c")
        for r,(name,nums) in enumerate([("商品A",[12,18,16]),("商品B",[9,11,15]),("商品C",[20,17,19])]):
            y=505+r*105
            d.rounded_rectangle((68,y-12,648,y+68),radius=8,fill="#ffffff" if r%2==0 else "#e4eef2")
            d.text((77,y),name,font=small,fill="#15364b")
            for c,v in enumerate(nums):
                value="…" if s==1 and c>=int(t*4) else str(v)
                d.text((222+c*145,y),value,font=med,fill="#126a78" if s>=2 else "#27485a")
        if s>=2:
            d.rounded_rectangle((65,828,655,900),radius=15,fill="#0c786f")
            d.text((92,843),"✓ 表形式で整理 / 要確認",font=med,fill="white")
        d.rounded_rectangle((40,960,680,1110),radius=20,fill="#123148")
        d.text((67,988),SCENES[s][1],font=med,fill="white")
        d.text((50,1170),f"{s+1:02d} / 04 | 投稿承認前",font=small,fill="#b8d4e2")
        d.rounded_rectangle((45,1230,45+int(630*(i+1)/144),1241),radius=4,fill="#57d5d0")
        im.save(frames/f"{i:04d}.png")
    dest=ROOT/"cycle1472_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","12","-i",str(frames/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(dest)],check=True)
    (ROOT/"captions.srt").write_text("".join(f"{i+1}\\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\\n{scene[1]}\\n\\n" for i,scene in enumerate(SCENES)),encoding="utf-8")
if __name__=="__main__":render()
