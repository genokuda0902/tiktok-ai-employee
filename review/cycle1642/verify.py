import json, subprocess, sys
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],text=True))
def quality(d):
    streams=d["streams"]
    v=next(s for s in streams if s["codec_type"]=="video")
    a=[s for s in streams if s["codec_type"]=="audio"]
    return {"video_ok":v["width"]==1080 and v["height"]==1920 and v["codec_name"]=="h264",
            "audio_stream_present":bool(a), "audio_codec":a[0]["codec_name"] if a else None,
            "japanese_narration_verified":False, "speech_caption_sync_verified":False,
            "publication_approved":False}
if __name__=="__main__":
    print(json.dumps(quality(probe(sys.argv[1])),ensure_ascii=False,indent=2))
