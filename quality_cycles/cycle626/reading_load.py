"""Cycle626 reusable editorial readability rules. Summaries are not transcripts."""
BOUNDARIES = [0, 70, 128, 178, 220, 287, 352, 415, 468]
SCENES = [
    ('これ、パソコン？', '手のひらサイズのPC', ''),
    ('小さくても本格派', 'Raspberry Pi 5', ''),
    ('モニターにつなぐ', 'ふつうのPC感覚', ''),
    ('接続して起動', '接続 → 電源 → 操作', ''),
    ('LEDを光らせる', 'コードで電子工作', ''),
    ('仕組みが見える', '入力 → 動作', ''),
    ('自分で作れる', 'アイデアを形に', ''),
    ('あとで試そう', '保存して挑戦！', ''),
]
PREVIOUS_SCENES = [
    ('この基板、実はPC。', '小さくても、立派なパソコン', 'CPUを搭載した超小型コンピューター。'),
    ('Raspberry Pi 5', 'カードほどのサイズ感', '小型でも、できることは本格派。'),
    ('小さなパソコン', 'モニターにつないで使う', '普段のPCに近い操作ができる。'),
    ('つなぐだけで動く', '接続 → 電源 → 操作', '使い始めるまでの基本ステップ。'),
    ('電子工作に挑戦', 'コードでLEDを光らせる', 'プログラミングを体験してみよう。'),
    ('仕組みが見える', '入力が動作につながる', 'センサーと制御のしくみを知る。'),
    ('作品をつくる', '自分だけの作品を作る', 'アイデアを動く形にしよう。'),
    ('気になったら保存', 'あとで試してみよう', '次の休日に、ひとつ作ってみよう。'),
]

def reading_load(scenes):
    """Counts alphanumeric glyphs across headline, card, and micro-description."""
    return [sum(ch.isalnum() for field in scene for ch in field) for scene in scenes]

def quality_gate(scenes=SCENES, previous=PREVIOUS_SCENES):
    if len(scenes) != 8 or len(previous) != 8:
        raise ValueError('Expected eight scenes')
    if any(len(s) != 3 for s in scenes):
        raise ValueError('Each scene requires headline, summary, description')
    if any(s[2] for s in scenes):
        raise ValueError('Micro-descriptions must be removed')
    now, old = reading_load(scenes), reading_load(previous)
    if any(n > 20 or n >= o for n, o in zip(now, old)):
        raise ValueError('On-screen text must be short and improve on baseline')
    if BOUNDARIES[0] != 0 or BOUNDARIES[-1] != 468 or len(BOUNDARIES) != 9:
        raise ValueError('Scene timeline is invalid')
    if any(b <= a for a, b in zip(BOUNDARIES, BOUNDARIES[1:])):
        raise ValueError('Scene boundaries must increase')
    return {'baseline_glyphs': sum(old), 'new_glyphs': sum(now),
            'reduction_pct': round((1 - sum(now) / sum(old)) * 100, 1),
            'baseline_per_scene': old, 'new_per_scene': now}
