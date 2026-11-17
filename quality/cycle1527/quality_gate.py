"""Fail-closed cross-genre media quality gate; stdlib only."""
import json, subprocess
def inspect(path, narration_verified=False, subtitles_verified=False, rights_approved=False, human_approved=False):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=next((s for s in data["streams"] if s["codec_type"]=="audio"),None)
    decode=subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(path),"-f","null","-"],capture_output=True,text=True)
    checks={"video_present":bool(video),"portrait_720_min":bool(video and video.get("width",0)>=720 and video.get("height",0)>=1280),"decodes":decode.returncode==0,"audio_stream_present":bool(audio),"japanese_narration_verified":bool(audio and narration_verified),"speech_subtitle_sync_verified":bool(subtitles_verified and audio and narration_verified),"source_rights_approved":rights_approved,"human_publication_approved":human_approved}
    return {"checks":checks,"publication_approved":all(checks.values()),"duration":float(data["format"]["duration"]),"video_codec":video.get("codec_name") if video else None,"audio_codec":audio.get("codec_name") if audio else None,"decode_error":decode.stderr[-1000:]}
if __name__=="__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
