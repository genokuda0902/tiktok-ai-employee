"""Fail-closed media QA for review MP4s."""
import json,subprocess,sys

def inspect(path):
 p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],capture_output=True,text=True,check=True)
 d=json.loads(p.stdout)
 v=next((s for s in d["streams"] if s["codec_type"]=="video"),None)
 a=next((s for s in d["streams"] if s["codec_type"]=="audio"),None)
 decode=subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],capture_output=True,text=True)
 return {"width":v["width"] if v else None,"height":v["height"] if v else None,"duration":float(d["format"]["duration"]),"video_codec":v["codec_name"] if v else None,"audio_codec":a["codec_name"] if a else None,"decode_ok":decode.returncode==0,"japanese_narration_verified":False,"subtitle_sync_verified":False,"rights_approved":False,"human_approved":False,"publication_approved":False}
if __name__=="__main__":print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
