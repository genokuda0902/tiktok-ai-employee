"""Review-only three-stage task-selection storyboard. Synthetic content, no publishing.

Draws one full-resolution, readable Japanese slide panel at a time. The panels
replace scene02's busy checklist while leaving the voice and burned subtitles
outside the panel untouched. Only explicitly allowlisted 10 genre examples.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 940, 1020
X, Y = 70, 350
VIDEO_W, VIDEO_H = 1080, 1920
CAPTION_TOP = 1450
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRE_TASKS = {
    'ai': ('週次報告をまとめる', '問い合わせを分類する', '会議の要点を整理する'),
    'beauty': ('ケアの手順を整理', '成分を比較', '使った感想を記録'),
    'romance': ('会話の要点を整理', '予定を調整', '気持ちを書き出す'),
    'saving': ('固定費を整理', '支出を分類', '買い物を振り返る'),
    'sales': ('商談メモを整理', '問い合わせを分類', '週次報告をまとめる'),
    'career': ('経験を書き出す', '求人条件を整理', '面接質問を用意'),
    'health': ('生活記録を整理', '相談内容をまとめる', '習慣を記録'),
    'trivia': ('疑問を整理', '情報源を確認', '要点をまとめる'),
    'travel': ('行き先を整理', '持ち物を確認', '旅程をまとめる'),
    'product_comparison': ('候補を整理', '仕様を比較', '条件をまとめる'),
}
POLICY = {'paid_service': False, 'auto_post': False, 'public_media_upload': False,
          'human_approval_required': True, 'unapproved_merge': False}
STAGE_TIMES = ((2.9, 3.83), (3.83, 4.80), (4.80, 5.80))


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    if Path(path).is_file():
        return ImageFont.truetype(path, size)
    # CI fallback: geometry and policy tests remain runnable without CJK fonts.
    return ImageFont.load_default(size=size)


def validate(genre, stage):
    if genre not in GENRE_TASKS:
        raise ValueError('genre not allowlisted')
    if stage not in (0, 1, 2):
        raise ValueError('invalid stage')
    if X < 0 or Y < 0 or X + W > VIDEO_W or Y + H > CAPTION_TOP:
        raise ValueError('caption or frame collision')
    if any(POLICY[k] for k in ('paid_service', 'auto_post', 'public_media_upload', 'unapproved_merge')):
        raise ValueError('release gate')
    if not POLICY['human_approval_required']:
        raise ValueError('human review must be required')
    tasks = GENRE_TASKS[genre]
    if len(tasks) != 3 or any(not s or len(s) > 17 for s in tasks):
        raise ValueError('invalid task labels')
    return tasks


def text(d, xy, value, size, color, bold=False):
    d.text(xy, value, font=font(size, bold), fill=color)


def render(path, stage, genre='ai'):
    tasks = validate(genre, stage)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Native-resolution opaque panel; no third-party media or personal data.
    d.rounded_rectangle((3, 4, W-4, H-4), radius=35, fill='#F4F8FE', outline='#C8D8E9', width=3)
    d.rounded_rectangle((4, 4, W-4, 165), radius=34, fill='#0D325E')
    d.rectangle((4, 125, W-4, 165), fill='#0D325E')
    text(d, (45, 27), '繰り返す作業を見つける', 49, '#FFFFFF', True)
    text(d, (46, 103), '毎週やっていることを、まず見える化', 28, '#9BEEE9')
    steps = ('01  洗い出す', '02  分けてみる', '03  1つ決める')
    for i, label in enumerate(steps):
        xx = 44 + i * 302
        selected = i == stage
        d.rounded_rectangle((xx, 188, xx+276, 258), radius=19,
                            fill='#18C7BC' if selected else '#E3EBF5')
        text(d, (xx+21, 200), label, 28, '#082B4D' if selected else '#52677D', True)
    if stage == 0:
        text(d, (50, 294), 'まずは「いつもの作業」を3つ書く', 36, '#123252', True)
        for i, task in enumerate(tasks):
            x = (53, 85, 59)[i]
            y = 368 + i * 129
            d.rounded_rectangle((x, y, W-54-(i%2)*27, y+106), radius=22,
                                fill='#FFFFFF', outline='#C9D8E8', width=3)
            d.rounded_rectangle((x+18, y+22, x+78, y+83), radius=16, fill='#D7F6F2')
            text(d, (x+36, y+31), str(i+1), 31, '#067C79', True)
            text(d, (x+104, y+23), task, 36, '#18364F', True)
        foot = '書き出すだけで、候補が見えてくる'
    elif stage == 1:
        text(d, (50, 294), '繰り返しが多いものから確認', 36, '#123252', True)
        for i, task in enumerate(tasks):
            y = 371 + i * 127
            selected = i == 0
            d.rounded_rectangle((50, y, W-51, y+106), radius=22,
                                fill='#D9FAF4' if selected else '#FFFFFF',
                                outline='#10B9AD' if selected else '#D4DFEA', width=4 if selected else 2)
            d.rounded_rectangle((70, y+25, 130, y+83), radius=16,
                                fill='#00AFA4' if selected else '#E4ECF5')
            text(d, (88, y+31), str(i+1), 31, '#FFFFFF' if selected else '#56728A', True)
            text(d, (155, y+23), task, 36, '#123252', True)
        foot = 'ここでは「候補」を選ぶだけ'
    else:
        text(d, (50, 295), '最初の1つは、これにする', 38, '#123252', True)
        d.rounded_rectangle((48, 377, W-49, 634), radius=30,
                            fill='#D9FAF4', outline='#0EB8AC', width=5)
        d.rounded_rectangle((82, 411, 257, 474), radius=17, fill='#0E988F')
        text(d, (104, 423), '選んだ作業', 28, '#FFFFFF', True)
        text(d, (79, 510), tasks[0], 47, '#0B354B', True)
        text(d, (57, 665), '※ 実際の業務情報は入力前に確認', 27, '#57738A')
        foot = '整理してから、AIへの指示を考える'
    text(d, (57, 845), '次のステップは、具体的な指示づくり', 27, '#68849B')
    d.rounded_rectangle((43, 920, W-44, 987), radius=19, fill='#DCEBFD')
    text(d, (62, 933), foot, 28, '#244F78', True)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('output_dir')
    p.add_argument('--genre', default='ai')
    a = p.parse_args()
    for n in range(3):
        render(Path(a.output_dir)/f'stage_{n}.png', n, a.genre)
