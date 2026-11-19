"""Shared 10-genre video QA: fail closed, never infer narration from an AAC track."""
import json
from pathlib import Path

def validate(probe: dict, *, japanese_voice_verified=False, captions_verified=False, rights_approved=False, employee_approved=False):
    streams=probe.get("streams", [])
    video=next((s for s in streams if s.get("codec_type")=="video" or s.get("width")), {})
    duration=float(probe.get("format", {}).get("duration", 0))
    checks={
        "vertical_video": video.get("height",0)>video.get("width",0),
        "duration": 8<=duration<=60,
        "japanese_voice_verified": bool(japanese_voice_verified),
        "captions_verified": bool(captions_verified),
        "rights_approved": bool(rights_approved),
        "employee_approved": bool(employee_approved),
    }
    return {"checks":checks,"publication_approved":all(checks.values())}

if __name__=="__main__":
    import sys
    print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text())),ensure_ascii=False,indent=2))
