import json, sys
from pathlib import Path
HARD_FAIL={"typo","reading_error","subtitle_word_split"}
def evaluate(report):
    issues=set(report.get("issues",[]))
    if issues & HARD_FAIL: return False, "HARD_FAIL: "+",".join(sorted(issues & HARD_FAIL))
    score=int(report.get("score",0))
    return score>=85, f"SCORE={score}"
if __name__=="__main__":
    p=Path(sys.argv[1]); r=json.loads(p.read_text(encoding="utf-8"))
    ok,msg=evaluate(r); print(("PASS " if ok else "REJECT ")+msg)
    raise SystemExit(0 if ok else 2)
