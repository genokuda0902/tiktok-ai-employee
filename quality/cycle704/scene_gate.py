"""Ten-genre-safe hook, proof, narration and publication gates (cycle704)."""
from dataclasses import dataclass
GENRES=("AI仕事効率化","AIツール紹介","Excel活用","ビジネススキル","副業知識","デザイン","教育","科学","ガジェット","生活効率化")
ROWS=(("赤",1200),("青",2500),("緑",1000),("青",3500))
DURATIONS=(1.5,2.5,2.5,2.5,2.5,2.5,3.0,3.0)
CAPTIONS=("【結果】青の売上 6,000円","架空の売上データ4行","AIに関数を相談","SUMIFで条件付き合計","数式を入力","青の2行だけを集計","2,500 + 3,500 = 6,000","保存して見返そう")
SPEECH=("青の売上は六千円。","これは架空の売上データです。","エーアイに関数を相談します。","サムイフで条件付き合計。","エクセルに数式を入力。","青の二行だけを合計します。","二千五百と三千五百で、六千円。","保存してあとで試してみて。")
@dataclass(frozen=True)
class Scene:
    index:int
    start:float
    end:float
    caption:str
    speech:str
def scenes():
    result=[]; t=0.0
    for i,(d,c,s) in enumerate(zip(DURATIONS,CAPTIONS,SPEECH)):
        result.append(Scene(i,t,t+d,c,s));t+=d
    return result
def proof():
    vals=[value for color,value in ROWS if color=="青"]
    return {"matches":len(vals),"sum":sum(vals),"formula":'=SUMIF(A2:A5,"青",B2:B5)'}
def hook_pass():
    first=scenes()[0]
    return first.start==0 and first.end<=1.5 and "6,000円" in first.caption and proof()["sum"]==6000
def speech_windows(lengths):
    if len(lengths)!=8:raise ValueError("speech segments missing")
    out=[]
    for sc,length in zip(scenes(),lengths):
        if not .15<length<=sc.end-sc.start-.10:raise ValueError("speech overrun")
        out.append({"start":sc.start,"end":round(sc.start+length,3),"scene":sc.index})
    return out
def publication_gate(assets_ok,private_data,narration_ok,sync_ok,employee_approved):
    return "READY_FOR_MANUAL_POST" if all((assets_ok,not private_data,narration_ok,sync_ok,employee_approved)) else "PUBLICATION_NOT_APPROVED"
