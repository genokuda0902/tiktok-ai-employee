"""Basic 10-genre-compatible QC; requires ffprobe and an MP4 argument."""
import json,subprocess,sys
def validate(path):
    info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path]))
    streams=info["streams"]
    video=next(s for s in streams if s["codec_type"]=="video")
    audio=next(s for s in streams if s["codec_type"]=="audio")
    assert (video["width"],video["height"],video["codec_name"])==(1080,1920,"h264")
    assert audio["codec_name"]=="aac"
    assert float(info["format"]["duration"])>1
    subprocess.run(["ffmpeg","-v","error","-i",path,"-f","null","-"],check=True)
if __name__=="__main__": validate(sys.argv[1])
