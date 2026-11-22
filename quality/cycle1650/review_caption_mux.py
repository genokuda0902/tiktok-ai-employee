"""Review-only caption mux and stream QA. Requires ffmpeg and ffprobe."""
import json
import subprocess
import sys
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True))

def review(path):
    data=probe(path)
    streams=data["streams"]
    video=next((s for s in streams if s["codec_type"]=="video"),None)
    captions=[s for s in streams if s["codec_type"]=="subtitle"]
    audio=[s for s in streams if s["codec_type"]=="audio"]
    return {"resolution_ok":bool(video and video["width"]==1080 and video["height"]==1920),
            "subtitle_track_present":bool(captions),
            "japanese_narration_verified":False,
            "audio_stream_present":bool(audio),
            "publication_allowed":False}

def mux(video,srt,out):
    subprocess.run(["ffmpeg","-y","-i",str(video),"-i",str(srt),"-map","0:v","-map","1:0","-c:v","copy","-c:s","mov_text","-metadata:s:s:0","language=jpn","-movflags","+faststart",str(out)],check=True)
    return review(out)

if __name__=="__main__":
    print(json.dumps(mux(*map(Path,sys.argv[1:4])),ensure_ascii=False,indent=2))
