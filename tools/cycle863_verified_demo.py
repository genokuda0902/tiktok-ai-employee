"""cycle863 reusable, zero-cost verified computation for TikTok slideshow demos.

The data are fictional. This is NOT a recording of an AI product.
Full local MP4 renderer and QA are shipped in cycle863_review_package.zip.
"""
SCENE_BOUNDS=(0,99,177,255,342,429,519,597,691)
FPS=30
GENRE_ACCENTS={
 "ai_productivity":"#3DD6BE","career":"#F6B85E","money":"#76D6A1",
 "health":"#86C8F8","learning":"#C5A9F8","beauty":"#F5A0C3",
 "travel":"#75C9F6","food":"#F5AF77","home":"#A5DB88",
 "business":"#7DA9FF"}
SAMPLE_TASKS=(("資料整理",True),("日報作成",True),("数値確認",True),("最終確認",False))

def compute_progress(tasks=SAMPLE_TASKS):
    if not tasks:
        raise ValueError("Tasks must not be empty")
    if any(not isinstance(done,bool) for _,done in tasks):
        raise TypeError("Completion flags must be bool")
    done=sum(1 for _,flag in tasks if flag)
    return {"total":len(tasks),"done":done,"pending":len(tasks)-done,
            "percent":round(done/len(tasks)*100)}

def generate_email(stats,limit=150):
    conclusion=f"今週の進捗は{stats['total']}件中{stats['done']}件完了、達成率{stats['percent']}%です。"
    pending=f"未完了{stats['pending']}件は明日確認します。"
    result=pending+conclusion
    if len(result)>limit:
        raise ValueError("Text exceeds length limit")
    return result

def revise_conclusion_first(text):
    parts=[x+"。" for x in text.split("。") if x]
    return "".join([x for x in parts if "達成率" in x]+
                   [x for x in parts if "達成率" not in x])

def scene_at(t):
    frame=min(690,max(0,int(t*FPS)))
    return next(i for i in range(8)
                if SCENE_BOUNDS[i]<=frame<SCENE_BOUNDS[i+1])

def demo_payload():
    stats=compute_progress()
    before=generate_email(stats)
    after=revise_conclusion_first(before)
    return {"synthetic":True,"input":SAMPLE_TASKS,
            "stats":stats,"before":before,"after":after,
            "within_150_chars":len(after)<=150}

if __name__=="__main__":
    import json
    print(json.dumps(demo_payload(),ensure_ascii=False,indent=2))
