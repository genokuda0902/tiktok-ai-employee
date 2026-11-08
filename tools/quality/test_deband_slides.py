import json, subprocess, sys
p = sys.argv[1]
probe = json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",p]))
streams=probe["streams"]
video=next(s for s in streams if s["codec_type"]=="video")
assert (video["width"],video["height"])==(1080,1920)
assert video["codec_name"]=="h264"
assert any(s["codec_type"]=="audio" and s["codec_name"]=="aac" for s in streams)
assert any(s["codec_type"]=="subtitle" for s in streams)
assert float(probe["format"]["duration"])>5
subprocess.run(["ffmpeg","-v","error","-i",p,"-f","null","-"],check=True)
print("PASS: vertical H264, AAC, subtitles, full decode")
