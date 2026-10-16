"""Cross-genre Japanese caption layout and honest, scene-specific lower-third.

Pure local graphics; no external asset, cloud call, or narration claim.
"""
from PIL import ImageFont

STAGE_HINTS = {
    'hook': 'このあと実演で確認',
    'problem': 'BEFORE｜手作業の負担',
    'prompt': 'AIへの質問例を表示',
    'select': 'STEP 1｜範囲を選択',
    'formula': 'STEP 2｜数式を入力',
    'proof': 'STEP 3｜数字を検算',
    'compare': 'BEFORE / AFTER',
    'cta': '保存して次回の集計で試す',
}

def caption_size(text, font_path, max_width=462, preferred=35, minimum=22):
    """Largest whole-pixel font that fits the fixed TikTok-safe caption line."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError('empty caption')
    for size in range(preferred, minimum-1, -1):
        f = ImageFont.truetype(font_path, size)
        if f.getlength(text) <= max_width:
            return size
    raise ValueError('caption too long for readable single-line layout')

def stage_hint(kind):
    if kind not in STAGE_HINTS:
        raise ValueError('unknown scene kind')
    return STAGE_HINTS[kind]

def scene_index(frame, scenes):
    if frame < 0 or frame >= scenes[-1][1]:
        raise ValueError('frame outside timeline')
    for i, (start, end, _caption, _kind) in enumerate(scenes):
        if start <= frame < end:
            return i
    raise ValueError('timeline gap')
