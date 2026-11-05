"""Cycle1239: safe synthetic spreadsheet storyboard; no publication approval."""
SCENES = [
    {"label":"BEFORE","heading":"手作業で集計","total":"?"},
    {"label":"ACTION","heading":"SUM関数を入力","total":"=SUM(B2:B3)"},
    {"label":"AFTER","heading":"合計を自動計算","total":"300"},
]
def validate(scenes):
    if len(scenes)!=3 or [s["label"] for s in scenes]!=["BEFORE","ACTION","AFTER"]:
        raise ValueError("Before/Action/After sequence required")
    if scenes[-1]["total"] != "300":
        raise ValueError("Synthetic example expected 120+180=300")
    return True
def scene_plan():
    validate(SCENES)
    return [{"start":i*6,"end":(i+1)*6,**scene} for i,scene in enumerate(SCENES)]
