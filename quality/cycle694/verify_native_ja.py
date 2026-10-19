#!/usr/bin/env python3
"""Cycle694: check real Open JTalk WAV, subtitle timing, and MP4 decode."""
import json,math,subprocess,sys,wave
from pathlib import Path

def check(folder):
    folder=Path(folder)
    report=json.loads((folder/"qa.json").read_text(encoding="utf-8"))
    assert report["native_ja"] is True and len(report["segments"])==4
    assert sum(report["values"])==report["sum"]==650
    for i,segment in enumerate(report["segments"]):
        wav=folder/f"ja{i}.wav"
        with wave.open(str(wav),"rb") as f:
            n=f.getnframes();sr=f.getframerate();frames=f.readframes(n)
        assert n>sr//3, (i,n,sr)
        assert len(frames)>n, "audio samples missing"
        assert segment["start"]<segment["end"]<=i*5+4.9
        assert any(ord(ch)>127 for ch in segment["spoken"])
        assert segment["caption"]
    mp4=folder/"cycle693_native_JA_REVIEW_ONLY.mp4"
    meta=json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_streams","-show_format","-of","json",str(mp4)
    ]))
    video=next(s for s in meta["streams"] if s["codec_type"]=="video")
    audio=next(s for s in meta["streams"] if s["codec_type"]=="audio")
    assert (video["width"],video["height"])==(1080,1920)
    assert video["codec_name"]=="h264" and audio["codec_name"]=="aac"
    assert abs(float(meta["format"]["duration"])-20)<.2
    subprocess.run(["ffmpeg","-v","error","-i",str(mp4),"-f","null","-"],check=True)
    out={"cycle":694,"native_japanese_waveforms":4,"timed_captions":4,
         "video_decode":"PASS","resolution":"1080x1920","duration_seconds":20,
         "review_only":True,"human_listening":"NOT VERIFIED",
         "reference_equivalence":False,"publication_approved":False}
    (folder/"cycle694_validation.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False))
if __name__=="__main__":
    check(sys.argv[1] if len(sys.argv)>1 else "output/cycle694_ci")
