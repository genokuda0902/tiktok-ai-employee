from pathlib import Path
import json, subprocess
root=Path(__file__).resolve().parent
manifest=json.loads((root/"manifest.json").read_text())
assert manifest["publication_allowed"] is False
assert manifest["narration_verified"] is False
assert manifest["burned_timed_explanatory_captions"] is True
video=root/"cycle1377_REVIEW_ONLY.mp4"
assert video.exists()
streams=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(video)]))["streams"]
assert any(s["codec_type"]=="video" and s["width"]==1080 and s["height"]==1920 for s in streams)
assert not any(s["codec_type"]=="audio" for s in streams)
subprocess.run(["ffmpeg","-v","error","-i",str(video),"-f","null","-"],check=True)
