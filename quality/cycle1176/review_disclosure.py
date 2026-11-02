#!/usr/bin/env python3
"""Review-only source-video disclosure repair. No assets are bundled or published."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY = "HUMAN_REVIEW/PUBLICATION_NOT_APPROVED"
GENRES = ("ai","business","money","learning","health","food","travel","beauty","career","life")
PANEL = (38,1290,1042,1432)
CAPTION_START = 1480
TEXT = "未承認｜社員確認後に手動投稿"
BG, FG, WARNING = "#081627", "#FFFFFF", "#FF7684"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def run(cmd):
    p = subprocess.run([str(x) for x in cmd],capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-3000:])
    return p.stdout

def sha(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1048576),b""):
            h.update(block)
    return h.hexdigest()

def probe(path):
    j=json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path]))
    v=next(x for x in j["streams"] if x["codec_type"]=="video")
    a=next(x for x in j["streams"] if x["codec_type"]=="audio")
    return {"duration":float(j["format"]["duration"]),"frames":int(v.get("nb_frames") or 0),
            "size":[v["width"],v["height"]],"fps":v["avg_frame_rate"],
            "video":v["codec_name"],"audio":a["codec_name"],"sample_rate":int(a["sample_rate"])}

def luminance(c):
    v=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    z=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in v]
    return sum(a*b for a,b in zip(z,(0.2126,0.7152,0.0722)))

def contrast(a,b):
    high,low=sorted((luminance(a),luminance(b)),reverse=True)
    return (high+0.05)/(low+0.05)

def validate(m,source):
    if (m.get("policy")!=POLICY or m.get("asset_approval")!="review_only_no_publication"
        or m.get("manual_post_only") is not True
        or m.get("disclosure_roi_reviewed") is not True
        or m.get("genre") not in GENRES):
        raise ValueError("Review-only approval gate failed")
    if m.get("source_sha256")!=sha(source):
        raise ValueError("Source SHA mismatch")
    p=probe(source)
    if (p["size"],p["fps"],p["video"],p["audio"],p["sample_rate"])!=([1080,1920],"30/1","h264","aac",48000):
        raise ValueError("Unsupported source stream")
    if not (0<=m["start"]<m["end"]<=p["duration"]+0.01):
        raise ValueError("Bad disclosure interval")
    if PANEL[3]>=CAPTION_START or contrast(FG,BG)<7:
        raise ValueError("Caption overlap or low contrast")
    return p

def make_overlay(path,font_path=FONT):
    if not Path(font_path).exists():
        raise FileNotFoundError(font_path)
    im=Image.new("RGBA",(1080,1920),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle(PANEL,radius=19,fill=BG,outline=WARNING,width=3)
    d.rounded_rectangle((57,1322,70,1400),radius=6,fill=WARNING)
    font=ImageFont.truetype(font_path,43)
    if d.textbbox((0,0),TEXT,font=font)[2]>900:
        raise ValueError("Disclosure text overflows")
    d.text((98,1326),TEXT,font=font,fill=FG)
    im.save(path)

def adts_sha(path):
    return hashlib.sha256(run(["ffmpeg","-v","error","-i",path,"-map","0:a:0","-c:a","copy","-f","adts","pipe:1"])).hexdigest()

def render(source,output,manifest,report,overlay):
    source,output,manifest,report,overlay=map(Path,(source,output,manifest,report,overlay))
    if source.resolve()==output.resolve():
        raise ValueError("Refuse to overwrite source")
    m=json.loads(manifest.read_text(encoding="utf-8"))
    before=validate(m,source)
    overlay.parent.mkdir(parents=True,exist_ok=True)
    make_overlay(overlay)
    output.parent.mkdir(parents=True,exist_ok=True)
    graph=f"[0:v][1:v]overlay=0:0:enable='gte(t,{m['start']})*lt(t,{m['end']})':eof_action=pass:format=auto,format=yuv420p[v]"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",source,
         "-loop","1","-framerate","30","-i",overlay,"-filter_complex",graph,
         "-map","[v]","-map","0:a:0","-c:v","libx264","-preset","veryfast","-crf","20",
         "-threads","4","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",
         "-t",str(before["duration"]),output])
    run(["ffmpeg","-v","error","-xerror","-i",output,"-f","null","-"])
    after=probe(output)
    audio_same=adts_sha(source)==adts_sha(output)
    passed=(audio_same and before["frames"]==after["frames"]
            and abs(before["duration"]-after["duration"])<0.05)
    result={"policy":POLICY,"source_sha256":sha(source),"output_sha256":sha(output),
            "before":before,"after":after,"overlay_time":[m["start"],m["end"]],
            "panel":PANEL,"caption_safe_start":CAPTION_START,"text":TEXT,
            "text_contrast_ratio":round(contrast(FG,BG),2),"aac_adts_bit_identical":audio_same,
            "full_av_decode":True,"technical_pass":passed,"independent_japanese_asr":False,
            "subtitle_semantic_sync_verified":False,"smartphone_verified":False,
            "rights_approved":False,"employee_approved":False,"publication_approved":False}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    if not passed:
        raise RuntimeError("Audio/video technical validation failed")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("source","output","manifest","report","overlay"):
        p.add_argument("--"+name,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report,a.overlay),ensure_ascii=False,indent=2))
