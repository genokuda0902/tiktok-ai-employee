"""Cycle627 reusable, zero-cost editorial contract for original vector slides.
This module is independent of the local Pillow/FFmpeg renderer and is safe to import
from any of the 10 genres. It does not authorize publishing.
"""
from dataclasses import dataclass

FPS=30
WIDTH=1080
HEIGHT=1920
FRAME_BOUNDARIES=(0,70,128,178,220,287,352,415,468)
TITLES=(
    "これ、パソコン？","小さくても本格派","モニターにつなぐ",
    "接続して起動","LEDを光らせる","仕組みが見える",
    "自分で作れる","あとで試そう",
)
CAPTIONS=(
    "手のひらサイズのPC","Raspberry Pi 5","ふつうのPC感覚",
    "接続 → 電源 → 操作","コードで電子工作","入力 → 動作",
    "アイデアを形に","保存して挑戦！",
)
GENRE_THEMES={
    "AI・仕事効率化":"#39e6cc",
    "美容・身だしなみ":"#e9b6cb",
    "恋愛・心理":"#f0a2a2",
    "お金・節約":"#d6dd80",
    "営業・ビジネス":"#5bcce0",
    "転職・キャリア":"#c0b1ff",
    "健康・生活改善":"#8bd1a8",
    "雑学・科学":"#55ebc8",
    "旅行・グルメ":"#f2c88d",
    "商品比較・暮らし":"#94c6f7",
}
STATUS="HUMAN_REVIEW"
PUBLICATION="NOT_APPROVED"
CAPTION_ALIGNMENT="scene-summary-not-word-aligned"

@dataclass(frozen=True)
class Scene:
    index:int
    start_frame:int
    end_frame:int
    title:str
    caption:str
    def seconds(self):
        return (self.end_frame-self.start_frame)/FPS

def scenes():
    return tuple(Scene(i+1,FRAME_BOUNDARIES[i],FRAME_BOUNDARIES[i+1],TITLES[i],CAPTIONS[i]) for i in range(8))

def validate():
    assert (WIDTH,HEIGHT,FPS)==(1080,1920,30)
    assert len(GENRE_THEMES)==10
    assert len(TITLES)==len(CAPTIONS)==8
    assert FRAME_BOUNDARIES[0]==0 and FRAME_BOUNDARIES[-1]==468
    assert all(a<b for a,b in zip(FRAME_BOUNDARIES,FRAME_BOUNDARIES[1:]))
    assert all(len(s.title)>0 and len(s.caption)>0 for s in scenes())
    assert STATUS=="HUMAN_REVIEW" and PUBLICATION=="NOT_APPROVED"
    return True
