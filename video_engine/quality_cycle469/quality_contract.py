"""Review-only scene/timeline gate. Technical checks never imply publishing approval."""
def validate_plan(plan):
    errors=[]
    scenes=plan.get("scenes",[])
    if not 6<=len(scenes)<=12: errors.append("scene_count")
    if not 15<=float(plan.get("duration",0))<=25: errors.append("duration")
    for key,expected in [("publication","NOT_APPROVED"),("quality","HUMAN_REVIEW"),("auto_post",False),("human_approval",False),("rights","ORIGINAL_SYNTHETIC"),("privacy","NO_REAL_PERSONAL_DATA"),("narration_status","NOT_GENERATED")]:
        if plan.get(key)!=expected: errors.append(key)
    if not scenes: return errors+["missing_scenes"]
    prev=0.
    for i,s in enumerate(scenes):
        a,b=float(s.get("start",-1)),float(s.get("end",-1))
        if abs(a-prev)>1e-6 or b<=a: errors.append(f"continuity_{i}")
        if not str(s.get("caption","")).strip(): errors.append(f"caption_{i}")
        prev=b
    if abs(prev-float(plan.get("duration",0)))>1e-6: errors.append("end")
    if float(scenes[0].get("end",999))>1.5: errors.append("hook_late")
    return errors
