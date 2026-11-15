"""Review-only caption safety and stream QA. Standard library only."""
import json
import subprocess
import sys
from pathlib import Path

def check(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
    streams=data["streams"]
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    assert video is not None, "video stream missing"
    assert video["height"]>video["width"], "not portrait"
    assert int(video["width"])>=720, "low resolution"
    assert not any(s.get("codec_type")=="audio" for s in streams), "audio needs separate Japanese narration verification"
    subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(path),"-f","null","-"],check=True)
    return {"resolution":f'{video["width"]}x{video["height"]}',"duration":float(data["format"]["duration"]),"japanese_narration_verified":False,"publication_approved":False}

if __name__=="__main__":
    print(json.dumps(check(Path(sys.argv[1])),ensure_ascii=False,indent=2))
