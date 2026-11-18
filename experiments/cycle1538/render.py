"""Reproducible public-safe REVIEW_ONLY demo. Requires ffmpeg, ffprobe, Japanese font. No TTS."""
import json, math, struct, subprocess, sys, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FONT=subprocess.check_output(["fc-match","-f","%{file}","Noto Sans CJK JP"],text=True).strip()
SCENES=[("課題","合計を毎回手計算していませんか？"),("操作","SUM関数でまとめて計算"),("実演","=SUM(B2:B5)"),("結果","4件の合計を一瞬で表示")]
def run(args): subprocess.run(args,check=True)
def esc(s): return s.replace("\\","\\\\").replace(":","\\:").replace("'","’").replace("%","\\%")
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    sr=24000
    with wave.open(str(ROOT/"cues.wav"),"wb") as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(sr)
        for n in range(sr*12):
            t=n/sr;p=t%3;env=max(0,1-p/.16) if p<.16 else 0
            wav.writeframesraw(struct.pack("<h",int(32767*.1*env*math.sin(2*math.pi*(540+60*(int(t)//3))*t))))
    vf=[]
    for i,(tag,body) in enumerate(SCENES):
        a=i*3;b=a+3
        vf.extend([f"drawbox=x=54:y=220:w=612:h=820:color=0x15253b:t=fill:enable='between(t,{a},{b})'",
                   f"drawtext=fontfile={FONT}:text='{esc(tag)}':fontcolor=0x53e0c5:fontsize=54:x=86:y=310:enable='between(t,{a},{b})'",
                   f"drawtext=fontfile={FONT}:text='{esc(body)}':fontcolor=white:fontsize=37:x=86:y=495:enable='between(t,{a},{b})'"])
    vf.append("drawbox=x=55:y=1120:w='610*t/12':h=12:color=0x53e0c5:t=fill")
    base=ROOT/"base.mp4";out=ROOT/"cycle1538_REVIEW_ONLY.mp4"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","color=c=0x08121f:s=720x1280:r=24:d=12","-i",str(ROOT/"cues.wav"),"-vf",",".join(vf),"-c:v","libx264","-preset","ultrafast","-crf","26","-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-t","12",str(base)])
    def ts(n): return f"00:00:{n:02d},000"
    srt="".join(f"{i+1}\\n{ts(i*3)} --> {ts((i+1)*3)}\\n{body}\\n\\n" for i,(_,body) in enumerate(SCENES)).replace("\\n","\n")
    (ROOT/"captions_ja.srt").write_text(srt,encoding="utf-8")
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(base),"-i",str(ROOT/"captions_ja.srt"),"-map","0:v:0","-map","0:a:0","-map","1:0","-c:v","copy","-c:a","copy","-c:s","mov_text","-metadata:s:s:0","language=jpn","-movflags","+faststart",str(out)])
    run(["ffmpeg","-v","error","-xerror","-i",str(out),"-f","null","-"])
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(out)]))
    (ROOT/"probe.json").write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding="utf-8")
    types={s["codec_type"] for s in probe["streams"]}
    assert {"video","audio","subtitle"}<=types
    assert any(s.get("width")==720 and s.get("height")==1280 for s in probe["streams"])
    assert 11.9<float(probe["format"]["duration"])<12.1
    print("PASS video/audio-cues/selectable-Japanese-captions; FAIL narration/speech-sync/approval")
if __name__=="__main__":main()
