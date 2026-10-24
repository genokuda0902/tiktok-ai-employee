"""Cycle812 shared semantic storyboard contract; no posting capability."""
from __future__ import annotations
from dataclasses import dataclass

WIDTH, HEIGHT, FPS = 1080, 1920, 30
GENRES = ("ai_work","beauty","love_psychology","money_saving","sales_business","career","health_life","science","travel_food","product_life")
ACCENTS = ("#63D7FF","#FF9CC8","#D5A8FF","#9CE9AC","#69E8CC","#88ACFF","#AEE68D","#75C9FF","#FFC17C","#B9A7FF")
SAFE_CAPTION_RECT = (74, 1225, 863, 1519)
RIGHT_UI_RESERVED_X = 890
BOTTOM_UI_RESERVED_Y = 1540
POSTING_ENABLED = False
EMPLOYEE_APPROVED = False
SCENE_TYPES = ("portrait_question","target","kpi_bars","one_priority","why_chain","action_checklist","feedback_loop","portrait_team")
HEADLINES = (
    ("できる人は","質問が違う。"),
    ("まず決める","目指すゴール"),
    ("感覚より","現状の数字"),
    ("差を見つけ","課題を一つに"),
    ("原因を深掘り","なぜ？を３回"),
    ("対策は具体的に","今日の行動へ"),
    ("結果を確かめ","すぐに改善"),
    ("小さな改善が","チームを強くする"),
)
CHUNKS = (
    ("仕事ができる人は、","質問が","違う。"),
    ("まず、","目指すゴールを","確認する。"),
    ("次に、","今の数字を","確かめる。"),
    ("そして、","理想との差を","一つに絞る。"),
    ("原因には、","なぜを三回","重ねる。"),
    ("対策は、","今日できる行動に","変える。"),
    ("結果を見て、","また","修正する。"),
    ("小さな改善が、","強いチームを","つくる。"),
)
def allocate_frames(total, chunks):
    """Allocate exact scene frames to three caption phases, >=5 each."""
    weights = [max(2,len(x.strip("、。"))) for x in chunks]
    base = [5]*len(weights)
    remainder = total-sum(base)
    if remainder < 0:
        raise ValueError("Scene shorter than 15 frames")
    raw = [remainder*w/sum(weights) for w in weights]
    add = [int(x) for x in raw]
    for i in sorted(range(len(weights)), key=lambda j:raw[j]-int(raw[j]), reverse=True)[:remainder-sum(add)]:
        add[i] += 1
    return [base[i]+add[i] for i in range(len(weights))]
def validate():
    assert len(GENRES)==len(set(GENRES))==10
    assert len(SCENE_TYPES)==len(HEADLINES)==len(CHUNKS)==8
    assert all(len(c)==3 for c in CHUNKS)
    assert SAFE_CAPTION_RECT[2]<RIGHT_UI_RESERVED_X
    assert SAFE_CAPTION_RECT[3]<BOTTOM_UI_RESERVED_Y
    assert (WIDTH,HEIGHT,FPS)==(1080,1920,30)
    assert not POSTING_ENABLED and not EMPLOYEE_APPROVED
    return True
if __name__ == "__main__":
    print("cycle812 semantic storyboard contract:",validate())
