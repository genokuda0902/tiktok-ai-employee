"""Reusable, zero-cost Japanese narration timeline for 10 genres. Review-only.

Requires open_jtalk + NAIST dictionary + Nitech voice; no network TTS API.
Never treat AAC presence as proof of spoken Japanese or posting approval.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, wave
from pathlib import Path
import numpy as np

SR=48000
BEATS=[
    (0,1.5,"まだ手で集計？","まだ手で集計してる？"),
    (1.5,4,"エーの行を三回選択。","Aの行を1つずつ探す"),
    (4,6.5,"架空の売上六行です。","6行の元データを確認"),
    (6.5,10,"サムイフ関数で、エーだけ集計。","Aチームの売上だけ集計"),
    (10,13,"十二、九、十四。合計三十五。","12＋9＋14＝35"),
    (13,16,"ビーは二十六。元データと一致。","計算結果は元データと一致"),
    (16,18.5,"手作業三回から、関数一つへ。","3回の選択から1つの関数へ"),
    (18.5,20,"保存して、試してね。","保存して、あとで試そう"),
]
def validate(beats=BEATS):
    if not beats or beats[0][0]!=0 or beats[0][1]>1.5 or beats[-1][1]!=20:
        raise ValueError("hook/timeline invalid")
    for i,(start,end,spoken,caption) in enumerate(beats):
        if end<=start or not spoken.strip() or not caption.strip():
            raise ValueError("invalid voice/caption beat")
        if i and start!=beats[i-1][1]:raise ValueError("timeline gap/overlap")
    return True

def run(cmd, input=None):
    p=subprocess.run(cmd,input=input,capture_output=True,text=True)
    if p.returncode:raise RuntimeError("command failed: "+" ".join(cmd)+"\n"+p.stderr[-1200:])
    return p.stdout

def pcm(path):
    with wave.open(str(path)) as w:
        if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getframerate()!=SR:
            raise ValueError("Expected 48k mono PCM16")
        return np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").astype(np.float32)/32768

def write(path, audio):
    with wave.open(str(path),"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes((np.clip(audio,-1,1)*32767).astype("<i2").tobytes())

def synthesize(folder, beats=BEATS):
    validate(beats)
    exe=shutil.which("open_jtalk")
    dic=Path("/var/lib/mecab/dic/open-jtalk/naist-jdic")
    model=Path("/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice")
    if not exe or not dic.is_dir() or not model.is_file():
        raise RuntimeError("Missing free Japanese TTS executable/dictionary/voice model")
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    track=np.zeros(20*SR,np.float32);timeline=[]
    for i,(start,end,spoken,caption) in enumerate(beats):
        wav=folder/f"voice_{i:02}.wav"
        run([exe,"-x",str(dic),"-m",str(model),"-r","1.18","-ow",str(wav)],input=spoken+"\n")
        raw=folder/f"voice_{i:02}_48k.wav"
        run(["ffmpeg","-y","-v","error","-i",str(wav),"-ar","48000","-ac","1","-c:a","pcm_s16le",str(raw)])
        samples=pcm(raw)
        slot=int((end-start-.12)*SR)
        if len(samples)>slot:
            factor=len(samples)/slot
            if factor>1.65:raise RuntimeError(f"Scene {i} narration too long: {factor:.2f}")
            samples=np.interp(np.linspace(0,len(samples)-1,slot),np.arange(len(samples)),samples).astype(np.float32)
        offset=int((start+.06)*SR)
        if offset+len(samples)>int(end*SR):raise RuntimeError("narration exceeds caption scene")
        track[offset:offset+len(samples)]+=samples*.84
        timeline.append(dict(scene=i,caption=caption,spoken=spoken,start=round(offset/SR,3),end=round((offset+len(samples))/SR,3),scene_end=end))
    if max(abs(track))<.003:raise RuntimeError("Narration is silent")
    out=folder/"narration.wav";write(out,track)
    (folder/"narration_timeline.json").write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding="utf-8")
    return out,timeline

def make_proof(folder, audio, beats=BEATS):
    """Only a technical spoken-audio proof. NOT the final creative renderer."""
    folder=Path(folder);ass=folder/"captions.ass"
    head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans CJK JP,68,&H00FFFFFF,&H000000FF,&H00201A08,&H80000000,1,0,0,0,100,100,0,0,1,3,0,5,80,80,250,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def fmt(t):return f"0:{int(t//60):02}:{int(t%60):02}.{int(t*100)%100:02}"
    ass.write_text(head+"".join(f"Dialogue: 0,{fmt(s)},{fmt(e)},Default,,0,0,0,,{caption}\n" for s,e,_,caption in beats),encoding="utf-8")
    video=folder/"cycle461_japanese_voice_technical_review.mp4"
    run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=0x10273e:s=1080x1920:r=30:d=20",
         "-i",str(audio),"-vf",f"subtitles={ass}", "-c:v","libx264","-preset","veryfast","-crf","23",
         "-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-t","20","-movflags","+faststart",str(video)])
    info=json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(video)]))
    v=next(s for s in info["streams"] if s["codec_type"]=="video")
    a=next(s for s in info["streams"] if s["codec_type"]=="audio")
    assert (v["width"],v["height"])==(1080,1920)
    assert v["codec_name"]=="h264" and a["codec_name"]=="aac"
    assert abs(float(info["format"]["duration"])-20)<.1
    run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"])
    qa={"cycle":461,"type":"TECHNICAL_VOICE_PROOF_NOT_CREATIVE_APPROVAL","voice_synthesized":True,
        "japanese_language_listening_verified":False,"caption_semantic_human_verified":False,
        "technical_scene_alignment":True,"full_decode":"PASS","publication":"NOT_APPROVED",
        "auto_post":False,"rights":"SYNTHETIC_ORIGINAL","sha256":hashlib.sha256(video.read_bytes()).hexdigest()}
    (folder/"QA_voice.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
    return video

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--outdir",required=True);a=ap.parse_args()
    wav,timeline=synthesize(a.outdir)
    video=make_proof(a.outdir,wav)
    print(json.dumps({"video":str(video),"narration":str(wav),"scenes":len(timeline),"status":"HUMAN_REVIEW_NOT_APPROVED"},ensure_ascii=False))
