"""Review-only video stream QA. Never equate stream presence with Japanese narration."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
    videos=[s for s in data["streams"] if s["codec_type"]=="video"]
    audios=[s for s in data["streams"] if s["codec_type"]=="audio"]
    if len(videos)!=1:
        raise ValueError("Expected exactly one video stream")
    v=videos[0]
    result={"width":v["width"],"height":v["height"],"fps":v.get("r_frame_rate"),
            "duration":float(data["format"]["duration"]),"audio_stream_present":bool(audios),
            "japanese_narration_verified":False,"speech_caption_sync_verified":False,
            "publication_approved":False}
    result["technical_video_pass"]=result["width"]==1080 and result["height"]==1920 and result["duration"]>0
    subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(path),"-f","null","-"],check=True)
    return result

if __name__=="__main__":
    import sys
    print(json.dumps(inspect(Path(sys.argv[1])),ensure_ascii=False,indent=2))
