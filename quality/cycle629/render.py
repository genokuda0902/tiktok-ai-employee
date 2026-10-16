"""Cycle629: synthetic, rights-safe caption-led video. REVIEW_ONLY."""
from PIL import Image,ImageDraw,ImageFont
import subprocess,json,sys,hashlib
from pathlib import Path
W,H=540,960
GENRES=("ai_work","beauty","relationships","money","sales_business","career","health_lifestyle","science_trivia","travel_food","product_lifestyle")
SCENES=[
("まだ手で集計？","4件のデータを確認",["120","150","200","250"]),
("数字を1つずつ確認","途中の値は確定ではない",["1月  120","2月  150","3月  200","4月  250"]),
("数式で検算","=SUM(B2:B5)",["B2 120","B3 150","B4 200","B5 250"]),
("結果は720","120+150+200+250",["検算済み","架空データ","実操作ではありません"])]
def check(genre="ai_work",rights="SYNTHETIC_REVIEW_ONLY",status="NOT_APPROVED"):
    if genre not in GENRES or rights!="SYNTHETIC_REVIEW_ONLY" or status!="NOT_APPROVED":raise ValueError("fail closed")
    if sum((120,150,200,250))!=720:raise ValueError("bad result")
    return True
def f(sz):
    return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",sz)
def draw(i):
    title,subtitle,rows=SCENES[i]
    im=Image.new("RGB",(W,H),(9,24,44));d=ImageDraw.Draw(im)
    for y in range(H):d.line((0,y,W,y),fill=(8+y//140,20+y//70,43+y//45))
    d.rounded_rectangle((24,80,516,132),radius=14,fill=(14,78,101))
    d.text((42,90),"AI時短ラボ / 数字の根拠",font=f(23),fill="white")
    d.text((32,185),title,font=f(43),fill=(252,229,121))
    d.rounded_rectangle((30,295,510,700),radius=22,fill=(18,61,84),outline=(41,219,234),width=3)
    for j,row in enumerate(rows):
        y=337+j*87
        d.rounded_rectangle((49,y,491,y+68),radius=10,fill=(32,105,125))
        d.text((68,y+12),row,font=f(28),fill="white")
    d.rounded_rectangle((26,758,514,845),radius=17,fill=(3,13,25),outline=(41,219,234),width=3)
    d.text((46,777),subtitle,font=f(26),fill="white")
    d.text((31,863),"SYNTHETIC / REVIEW ONLY",font=f(17),fill=(165,200,215))
    return im
def render(path,genre="ai_work"):
    check(genre);path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    frames=path.parent/"cycle629_frames";frames.mkdir(exist_ok=True)
    for i in range(4):draw(i).save(frames/f"{i}.png")
    playlist=frames/"concat.txt"
    playlist.write_text("".join(f"file '{frames/i.__str__() if False else str(frames/f'{i}.png')}'\nduration 5\n" for i in range(4))+f"file '{frames/'3.png'}'\n")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-safe","0","-f","concat","-i",str(playlist),
         "-f","lavfi","-i","sine=frequency=180:sample_rate=44100:duration=20",
         "-t","20","-vf","fps=30,scale=1080:1920:flags=lanczos,format=yuv420p",
         "-c:v","libx264","-preset","veryfast","-crf","21","-c:a","aac","-b:a","96k",
         "-movflags","+faststart",str(path)]
    subprocess.run(cmd,check=True)
    qa={"rights":"SYNTHETIC_REVIEW_ONLY","publication":"NOT_APPROVED","narration":"NONE",
        "subtitle":"TIMED_ON_SCREEN_NOT_SPEECH_SYNCED","width":1080,"height":1920,
        "duration_s":20,"genre":genre,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    path.with_suffix(".json").write_text(json.dumps(qa,ensure_ascii=False,indent=2))
    return qa
if __name__=="__main__":print(json.dumps(render(sys.argv[1] if len(sys.argv)>1 else "output/cycle629_REVIEW_ONLY.mp4"),ensure_ascii=False))
