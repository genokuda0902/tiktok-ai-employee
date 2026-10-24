"""Cycle821 GitHub Actions output checks. Technical validation, not editorial approval."""
import json,subprocess,sys,hashlib
from pathlib import Path
root=Path(sys.argv[1])
mp4=root/"output"/"cycle821_THREE_LINE_MOBILE_READABILITY_HUMAN_REVIEW.mp4"
ass=root/"output"/"captions817.ass"
data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(mp4)],text=True))
v=next(x for x in data["streams"] if x["codec_type"]=="video")
a=next(x for x in data["streams"] if x["codec_type"]=="audio")
lines=[s for s in ass.read_text().splitlines() if s.startswith("Dialogue:")]
captions=[s for s in lines if r"\pos(540,1235)" in s]
checks={
 "1080x1920":(v["width"],v["height"])==(1080,1920),
 "h264_30fps":v["codec_name"]=="h264" and v["r_frame_rate"]=="30/1",
 "775_frames":int(v.get("nb_frames",0))==775,
 "aac_48khz":a["codec_name"]=="aac" and a["sample_rate"]=="48000",
 "full_japanese_voice":float(a.get("duration",data["format"]["duration"]))>25.7,
 "24_three_line_subtitles":len(captions)==24 and all(s.count(r"\N")==2 for s in captions),
 "mobile_font_90":"Sans CJK JP,90," in ass.read_text(),
 "cta_safe_y":r"\pos(540,1590)" in ass.read_text(),
}
decode=subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(mp4),"-map","0:v:0","-f","null","-"],capture_output=True,text=True)
checks["full_decode"]=decode.returncode==0
out={"cycle":821,"checks":checks,"passed":sum(checks.values()),"total":len(checks),
 "sha256":hashlib.sha256(mp4.read_bytes()).hexdigest(),"publication_approved":False}
(root/"output"/"qa821_ci.json").write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
if not all(checks.values()):sys.exit(1)
