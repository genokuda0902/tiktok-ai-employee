import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def choose(metrics, ideas):
    seen={x.get("topic") for x in metrics[-30:]}
    def score(x):
        s=50
        if x.get("topic") not in seen: s+=15
        s+=min(20,int(x.get("hook_score",10)))
        if x.get("proven_format"): s+=10
        if x.get("risk"): s-=30
        return s
    return sorted(ideas,key=score,reverse=True)[:2]
if __name__=="__main__":
    print("AI editor brain ready")
