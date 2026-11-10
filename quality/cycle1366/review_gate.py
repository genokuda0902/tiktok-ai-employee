"""Evidence-based review gate for generated MP4; no fixed QA score."""
import json
import subprocess

def inspect(path):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height:format=duration","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    decode=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True,text=True)
    return {"width":video.get("width") if video else None,"height":video.get("height") if video else None,
            "duration":float(data["format"]["duration"]),"audio_codec":audio.get("codec_name") if audio else None,
            "full_decode_ok":decode.returncode==0}

def publication_allowed(evidence, human_approved=False):
    return bool(human_approved and evidence.get("full_decode_ok") and evidence.get("width")==1080
                and evidence.get("height")==1920 and evidence.get("audio_codec")
                and evidence.get("japanese_narration_verified")
                and evidence.get("speech_caption_sync_verified")
                and evidence.get("asset_rights_verified"))
