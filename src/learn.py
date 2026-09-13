import json
from pathlib import Path
def summarize(rows):
    valid=[r for r in rows if r.get("views",0)>0]
    for r in valid:
        r["follower_conversion"]=r.get("follower_gain",0)/max(1,r.get("views",0))
    best=sorted(valid,key=lambda x:(x.get("follower_conversion",0),x.get("shares",0)),reverse=True)[:5]
    return {"best_patterns":[{"topic":x.get("topic"),"hook":x.get("hook"),
             "follower_conversion":round(x["follower_conversion"],5)} for x in best],
            "rule":"Optimize follower gain per post; do not optimize views alone."}
if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]; out=root/"output"; out.mkdir(exist_ok=True)
    p=root/"data/history.json"
    rows=json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    (out/"learning.json").write_text(json.dumps(summarize(rows),ensure_ascii=False,indent=2),encoding="utf-8")
