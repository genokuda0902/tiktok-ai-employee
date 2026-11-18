"""Fail-closed genre-neutral MP4 publication quality gate."""
import json, subprocess, sys
def assess(probe, narration_verified=False, captions_verified=False, assets_approved=False, employee_approved=False):
    streams=probe.get("streams",[])
    v=next((s for s in streams if s.get("codec_type")=="video"),{})
    checks={
      "vertical":v.get("width",0)*16==v.get("height",0)*9 and v.get("width",0)>=720,
      "duration":5<=float(probe.get("format",{}).get("duration",0))<=60,
      "audio_present":any(s.get("codec_type")=="audio" for s in streams),
      "japanese_narration_verified":bool(narration_verified),
      "captions_verified":bool(captions_verified),
      "assets_approved":bool(assets_approved),
      "employee_approved":bool(employee_approved)}
    return {"checks":checks,"publication_approved":all(checks.values())}
def probe_file(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,codec_name,width,height","-of","json",path]))
if __name__=="__main__":
    print(json.dumps(assess(probe_file(sys.argv[1])),indent=2))
