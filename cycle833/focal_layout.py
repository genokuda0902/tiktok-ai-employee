"""Cycle 833 portable layout/genre core. No paid API or publishing functions.
This module is dependency-free. The local review package contains the full
Pillow/FFmpeg renderer and rights-gated image/audio assets.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

WIDTH, HEIGHT, FPS = 1080, 1920, 30
FRAMES = (101, 93, 91, 99, 98, 101, 89, 103)
PHOTO_RECT = (62, 390, 1018, 1390)
CAPTION_RECT = (60, 1452, 1020, 1790)
FOCUS_Y = (.27, .34, .25, .43, .39, .31, .36, .27)
GENRES = {
 "ai_work": ("#40DDCB", ("AIで仕事を早くする","繰り返す作業を探す","完成見本を用意する","目的と条件を伝える","AIの回答を確認する","修正点は一つずつ","良い指示を保存する","小さな時短を習慣に")),
 "sales_business": ("#F4B65C", ("営業の成果を変える","相手の悩みを聞く","結論を先に伝える","根拠を具体的に示す","質問の意図を確かめる","次の行動を提案する","良い会話を振り返る","改善を毎日続ける")),
 "beauty": ("#F4A8BC", ("自分らしい美容習慣","肌の状態を知る","刺激を減らしてみる","保湿を習慣にする","日差しから守る","使う量を見直す","変化を記録する","無理なく続ける")),
 "romance": ("#EBA9CD", ("伝わる会話のコツ","相手の話を最後まで","気持ちを言葉にする","期待を押しつけない","違いを認めてみる","感謝を伝える","小さな約束を守る","一緒に考えてみる")),
 "saving": ("#E9C970", ("今日から家計を整える","固定費を書き出す","支出を３つに分ける","先取り額を決める","無理のない予算に","週１回だけ確認","続く仕組みを作る","小さく積み上げる")),
 "career": ("#96B9FF", ("仕事の成長を加速","得意を言語化する","課題を一つに絞る","行動を数字で見る","相談の準備をする","振り返りを残す","次の挑戦を選ぶ","毎週改善を続ける")),
 "wellness": ("#A6DDB5", ("暮らしを整える習慣","睡眠時間を確保する","水分補給を意識","体を少し動かす","休憩を予定に入れる","無理せず調整する","体調の変化を見る","続けられる形に")),
 "science": ("#E7B28B", ("身近な科学を楽しむ","疑問を見つける","予想を立ててみる","条件を一つ変える","結果を記録する","別の説明も探す","根拠を確かめる","新しい疑問へ進む")),
 "travel_food": ("#C0A9F8", ("旅をもっと楽しく","行きたい場所を選ぶ","移動時間を調べる","予算を決めておく","食べたい物を探す","混雑時間を避ける","余白も予定に入れる","旅の思い出を残す")),
 "productivity": ("#88DCE1", ("毎日の作業を軽く","今日の目標を一つ","やらない事を決める","集中時間を作る","通知を少し減らす","休憩を先に予定","終わりに振り返る","明日の準備をする"))
}
@dataclass(frozen=True)
class Crop:
    resized_width: int
    resized_height: int
    left: int
    top: int
    width: int
    height: int

def focal_crop(src_width: int, src_height: int, width: int, height: int, focus_y: float) -> Crop:
    """Deterministic focal crop: equivalent geometry to local Pillow renderer."""
    if min(src_width,src_height,width,height) <= 0 or not 0 <= focus_y <= 1:
        raise ValueError("Invalid dimensions or focus")
    scale=max(width/src_width,height/src_height)
    rw,rh=math.ceil(src_width*scale),math.ceil(src_height*scale)
    left=(rw-width)//2
    top=max(0,min(rh-height,round(rh*focus_y-height*.5)))
    return Crop(rw,rh,left,top,width,height)

def progress_segments(scene_index: int, segments: int = 8) -> tuple[bool,...]:
    if not 0 <= scene_index < segments: raise ValueError("scene index out of range")
    return tuple(i <= scene_index for i in range(segments))

def validate_layout() -> None:
    assert len(GENRES)==10 and all(len(scenes)==8 for _,scenes in GENRES.values())
    assert len(FRAMES)==len(FOCUS_Y)==8 and sum(FRAMES)==775
    assert PHOTO_RECT[3] < CAPTION_RECT[1]
    assert CAPTION_RECT[3] <= 1800
