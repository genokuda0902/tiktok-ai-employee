#!/usr/bin/env python3
"""Cycle418 review-only Japanese narration + original mobile slide renderer.

Kokoro Japanese TTS must succeed. No phonetic fallback, no silent audio, no
external reference footage, no posting, and no publication approval.
"""
from pathlib import Path
import hashlib, json, math, subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

OUTPUT=Path("output/cycle418")
OUTPUT.mkdir(parents=True,exist_ok=True)
TEXTS=[
 "会議メモ、毎回手作業？",
 "担当と期限が埋もれがちです。",
 "決定事項、担当、期限の三項目に分けてください。",
 "表にすれば、確認する場所が一目で分かります。",
 "不明な期限は、推測せず要確認にします。",
 "個人情報と共有範囲も、必ず確認しましょう。",
 "次の会議メモで、試してみてください。"
]
TITLES=[
 "会議メモ、\nまだ手作業？","大事な情報が\n埋もれる","AIには\nこの指示",
 "表なら\n一目で分かる","不明な情報は\n推測しない",
 "共有前に\n必ず確認","次の会議から\n3項目で整理"
]
BODY=[
 ["決定事項","担当者","期限"],
 ["A案に決定・資料更新","Bさん、週明け確認","日程は次回相談"],
 ["① 決定事項","② 担当者","③ 期限","不明な点は『要確認』"],
 ["決定事項　　担当　　期限","資料を更新　 Aさん　金曜","日程を調整　 Bさん　要確認"],
 ["期限：未定","↓","期限：要確認"],
 ["01 氏名・連絡先","02 社外秘の内容","03 共有する相手"],
 ["決定事項・担当・期限","不明な点は要確認","保存して後で試す"]
]
GENRES=["ai_work","excel","documents","mail","study","finance","travel","recruit","sales","daily"]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
W,H,FPS,SR=1080,1920,30,24000

def sh(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        raise RuntimeError("command failed: "+" ".join(args)+"\n"+p.stderr[-1800:])
    return p.stdout

def scene_duration(samples):
    return max(2.35,math.ceil((len(samples)/SR+0.28)*FPS)/FPS)

def voice_segments():
    from kokoro import KPipeline
    pipe=KPipeline(lang_code="j")
    clips=[]
    for i,t in enumerate(TEXTS):
        waves=[np.asarray(a,dtype=np.float32) for _,_,a in pipe(t,voice="jf_alpha",speed=1.15)]
        if not waves: raise RuntimeError("Native Japanese TTS empty scene "+str(i+1))
        wav=np.concatenate(waves)
        if len(wav)<SR//3 or float(np.sqrt(np.mean(wav**2)))<0.001:
            raise RuntimeError("Native Japanese TTS silent scene "+str(i+1))
        if float(np.max(np.abs(wav)))>1.001: raise RuntimeError("Audio clipping")
        clips.append(wav)
    return clips

def slide(i):
    im=Image.new("RGB",(W,H),"#071528")
    d=ImageDraw.Draw(im)
    d.ellipse((710,-340,1490,440),fill="#0F3540")
    def txt(x,y,s,sz,color="#F8FAFF",bold=True):
        f=ImageFont.truetype(FONT if bold else FONT_REG,sz)
        d.multiline_text((x,y),s,font=f,fill=color,spacing=14)
    def box(b,fill,outline=None):
        d.rounded_rectangle(b,radius=28,fill=fill,outline=outline,width=4)
    box((75,74,695,140),"#154149")
    txt(98,88,"AI × 仕事効率化 / 会議メモ",32,"#61E4D0")
    txt(905,89,str(i+1).zfill(2)+"/07",31,"#A8C1D4")
    txt(78,205,TITLES[i],79)
    d.rounded_rectangle((85,432,85+round(915*(i+1)/7),446),radius=7,fill="#56E3CF")
    box((75,515,1000,1425),"#152A42","#34546A")
    for j,s in enumerate(BODY[i]):
        if len(BODY[i])==4:
            y=594+j*175
        else:
            y=605+j*215
        box((118,y,955,y+138),"#203B54")
        txt(150,y+32,s,44 if len(s)>16 else 53,"#FFCC6D" if "要確認" in s else "#F8FAFF")
    box((76,1510,1000,1645),"#0B2939","#407E83")
    txt(106,1539,TEXTS[i],37)
    txt(82,1705,"日本語TTS試作：発音・自然さは人間確認待ち",29,"#FFCC6D")
    txt(82,1760,"HUMAN_REVIEW / PUBLICATION_NOT_APPROVED",26,"#AFC5D6")
    txt(82,1830,"ORIGINAL SLIDES  •  NO AUTO POST",25,"#91A6B9")
    return im

def main():
    clips=voice_segments()
    all_audio=[]; durations=[]; levels=[]; video_files=[]
    for i,wav in enumerate(clips):
        sec=scene_duration(wav)
        n=round(sec*SR)
        if len(wav)>n: raise RuntimeError("Narration would be cut")
        full=np.pad(wav,(0,n-len(wav)))
        all_audio.append(full);durations.append(sec)
        levels.append(round(20*np.log10(max(float(np.sqrt(np.mean(wav**2))),1e-9)),1))
        png=OUTPUT/("slide_%02d.png"%(i+1))
        slide(i).save(png,optimize=True)
        part=OUTPUT/("clip_%02d.mp4"%(i+1))
        sh(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1",
            "-framerate","30","-i",str(png),"-vf",
            "zoompan=z='min(zoom+0.00028,1.025)':d=1:s=1080x1920:fps=30,format=yuv420p",
            "-frames:v",str(round(sec*FPS)),"-c:v","libx264","-preset",
            "ultrafast","-crf","23","-an",str(part)])
        video_files.append(part)
    if not 15<=sum(durations)<=25:
        raise RuntimeError("TikTok duration outside 15-25s: "+str(sum(durations)))
    sf.write(OUTPUT/"cycle418_voice.wav",np.concatenate(all_audio),SR,subtype="PCM_16")
    (OUTPUT/"concat.txt").write_text("".join("file '"+str(p.resolve())+"'\n" for p in video_files))
    mp4=OUTPUT/"cycle418_native_japanese_REVIEW_ONLY.mp4"
    sh(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0",
        "-i",str(OUTPUT/"concat.txt"),"-i",str(OUTPUT/"cycle418_voice.wav"),
        "-map","0:v","-map","1:a","-c:v","libx264","-preset","veryfast",
        "-crf","20","-c:a","aac","-b:a","128k","-ar","48000","-ac","1",
        "-movflags","+faststart","-shortest",str(mp4)])
    info=json.loads(sh(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(mp4)]))
    vs=[s for s in info["streams"] if s["codec_type"]=="video"]
    aud=[s for s in info["streams"] if s["codec_type"]=="audio"]
    if len(vs)!=1 or len(aud)!=1 or (vs[0]["width"],vs[0]["height"])!=(W,H):
        raise RuntimeError("Missing video/audio or wrong resolution")
    sh(["ffmpeg","-hide_banner","-loglevel","error","-i",str(mp4),"-f","null","-"])
    manifest={"cycle":418,"previous_reviewed_cycle":415,
      "native_japanese_tts_engine":"Kokoro-82M / jf_alpha / Japanese",
      "model_source":"hexgrad/Kokoro-82M (Apache-2.0)",
      "native_tts_generated":True,"human_listening_verified":False,
      "semantic_caption_sync_verified":False,"publication_approved":False,
      "auto_post":False,"scenes":7,"genre_templates":GENRES,
      "genres_e2e_verified":["ai_work"],"scene_durations":durations,
      "scene_audio_rms_dbfs":levels,"duration_s":float(info["format"]["duration"]),
      "codec_video":vs[0]["codec_name"],"codec_audio":aud[0]["codec_name"],
      "width":vs[0]["width"],"height":vs[0]["height"],
      "sha256":hashlib.sha256(mp4.read_bytes()).hexdigest(),
      "rights":"Original graphics and Apache-2.0 licensed Kokoro model; no user reference footage"}
    (OUTPUT/"cycle418_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__": main()
