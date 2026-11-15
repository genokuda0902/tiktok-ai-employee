"""Review-only QA: fail closed when Japanese speech is absent."""
import json, subprocess, sys

def inspect(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    decode=subprocess.run(["ffmpeg","-v","error","-i",path,"-f","null","-"],capture_output=True)
    return {"video_ok":bool(video) and decode.returncode==0,"resolution":[video.get("width"),video.get("height")] if video else None,"audio_present":bool(audio),"japanese_narration_verified":False,"speech_caption_sync_verified":False,"rights_approved":False,"employee_approved":False,"publication_approved":False}

if __name__=="__main__":
    print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
