"""Cycle1412 reproducible synthetic review renderer. No third-party assets."""
from pathlib import Path
import json, subprocess, hashlib
from PIL import Image, ImageDraw, ImageFont

SCENES = [
 ("集計が遅い原因は？", "手計算より、関数で確認", "hook"),
 ("架空の売上データ", "3,200円・4,100円・5,100円", "select"),
 ("SUM関数を入力", "合計セルに =SUM(B2:B4)", "type"),
 ("合計 12,400円", "計算結果を必ず確認しましょう", "result"),
 ("保存して試そう", "架空データでSUMを練習", "result"),
]
FPS = 12
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
ROOT = Path(__file__).resolve().parent

def scene_at(t):
    return min(4, int(t // 3))

def render():
    frames = ROOT / "frames"
    frames.mkdir(exist_ok=True)
    large = ImageFont.truetype(FONT, 38)
    medium = ImageFont.truetype(FONT, 30)
    for n in range(15 * FPS):
        i = scene_at(n / FPS)
        title, caption, action = SCENES[i]
        im = Image.new("RGB", (720, 1280), "#0b1425")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((35,145,685,1030),radius=30,fill="#172c43")
        d.rounded_rectangle((55,220,665,325),radius=15,fill="#225a72")
        d.text((70,245),title,font=large,fill="white")
        for j, value in enumerate(("3,200","4,100","5,100")):
            y = 420 + j*115
            active = action == "select" and j == min(2,int((n/FPS-3))) or action == "type"
            d.rounded_rectangle((100,y,625,y+90),radius=12,fill="#276d7d" if active else "#263b54")
            d.text((130,y+19),f"B{j+2}    {value}",font=medium,fill="white")
        if action == "type":
            formula = "=SUM(B2:B4)"
            shown = formula[:max(1,int(((n/FPS)-6)/3*len(formula)))]
            d.text((95,835),shown+"▏",font=medium,fill="#79f1d6")
        else:
            d.text((95,835),"12,400 円 ✓" if action == "result" else "B2:B4",font=medium,fill="#79f1d6")
        d.rounded_rectangle((40,1060,680,1175),radius=18,fill="#07121d")
        d.text((65,1085),caption,font=medium,fill="white")
        d.rectangle((0,1235,int(720*(n+1)/(15*FPS)),1246),fill="#4be2c7")
        im.save(frames / f"{n:04d}.jpg",quality=87)
    out = ROOT / "cycle1412_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(FPS),"-i",str(frames/"%04d.jpg"),"-vf","scale=1080:1920:flags=lanczos,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","25","-movflags","+faststart",str(out)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(out)]))
    streams=probe["streams"]
    qa={"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"duration":float(probe["format"]["duration"]),"width":streams[0]["width"],"height":streams[0]["height"],"audio_streams":sum(s["codec_type"]=="audio" for s in streams),"japanese_narration":"ABSENT","speech_synced_captions":"ABSENT","publication":"NOT_APPROVED","decode":"PASS"}
    (ROOT/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
    return qa
if __name__=="__main__":
    print(json.dumps(render(),ensure_ascii=False))
