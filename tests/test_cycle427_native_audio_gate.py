# cycle427: Japanese narration must be real, never simulated.
from pathlib import Path
import json, subprocess, sys
def probe(path):
    p=Path(path)
    if not p.exists() or not p.stat().st_size: raise RuntimeError("missing MP4")
    x=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)]))
    v=[s for s in x["streams"] if s["codec_type"]=="video"]
    a=[s for s in x["streams"] if s["codec_type"]=="audio"]
    assert len(v)==1 and (v[0]["width"],v[0]["height"])==(1080,1920)
    assert len(a)==1, "Real Japanese audio REQUIRED; silent preview not approved"
    assert 15<=float(x["format"]["duration"])<=25
    return True
if __name__=="__main__":probe(sys.argv[1])
