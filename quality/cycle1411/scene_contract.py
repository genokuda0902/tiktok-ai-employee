"""Reusable scene timeline contract for 10 content genres; no private assets."""
SCENES = [
    {"seconds": 3, "title": "その集計、まだ手入力？", "caption": "3件の売上を一瞬で合計する方法", "action": "hook"},
    {"seconds": 3, "title": "架空の売上データ", "caption": "3,200円・4,100円・5,100円", "action": "select"},
    {"seconds": 3, "title": "SUM関数を入力", "caption": "合計セルに =SUM(B2:B4)", "action": "type"},
    {"seconds": 3, "title": "合計 12,400円", "caption": "計算結果を必ず確認しましょう", "action": "result"},
]
def validate(scenes):
    if not scenes or any(not isinstance(s.get("seconds"),int) or s["seconds"]<=0 or not s.get("caption","").strip() for s in scenes):
        raise ValueError("invalid scene timeline")
    return sum(s["seconds"] for s in scenes)
def at(t, scenes=SCENES):
    validate(scenes)
    if t < 0: raise ValueError("negative time")
    elapsed=0
    for i,s in enumerate(scenes):
        if t < elapsed+s["seconds"]: return i,s,(t-elapsed)/s["seconds"]
        elapsed+=s["seconds"]
    return len(scenes)-1,scenes[-1],1.0
