#!/usr/bin/env python3
"""Reject silent TikTok review videos before publication."""
import json, subprocess, sys
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],text=True))
def validate(path):
    p=probe(path); v=[s for s in p["streams"] if s["codec_type"]=="video"]; a=[s for s in p["streams"] if s["codec_type"]=="audio"]
    assert v and v[0]["width"]==1080 and v[0]["height"]==1920, "invalid video size"
    assert a, "BLOCKED: Japanese narration absent"
    # An audio stream alone is not proof of intelligible Japanese speech.
    return "REVIEW_REQUIRED: check Japanese speech, synchronization and rights manually"
if __name__=="__main__":
    try: print(validate(sys.argv[1]))
    except (AssertionError,IndexError) as e: print(e,file=sys.stderr);sys.exit(2)
