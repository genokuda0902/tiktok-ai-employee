"""Reusable scene timing and quality validation for cycle494."""
GENRES = ("ai_work","business","sales","beauty","money","psychology","career","science","travel","comparison")
WIDTH, HEIGHT, FPS = 1080, 1920, 30
DATA = (120, 150, 200, 250)
SCENES = (
    ("hook",2.5,"手作業と自動化を比較"),
    ("source",3.0,"元データは４か月分"),
    ("prompt",3.0,"AIへの指示は具体的に"),
    ("formula",3.5,"SUM関数で検算する"),
    ("graph",4.0,"グラフも同じ数値から"),
    ("compare",2.0,"違いは手順の整理"),
    ("cta",2.0,"数字を確認して保存"),
)
def timeline():
    elapsed=0.0
    output=[]
    for kind,duration,caption in SCENES:
        output.append((kind,round(elapsed,3),round(elapsed+duration,3),caption))
        elapsed+=duration
    return output
def valid():
    return (len(GENRES)==10 and sum(DATA)==720 and
            sum(s[1] for s in SCENES)==20 and
            all(len(s[2])<=22 for s in SCENES))
