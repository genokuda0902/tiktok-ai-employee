#!/usr/bin/env python3
"""Review-only TikTok scene 05: explicit UNAPPROVED gate, never fabricated checkmarks."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
START, END = 348, 435  # scene 05, 11.6–14.5 seconds, 87 frames
CAPTION_SAFE_Y = 1460
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
    'ai_work': ('#24C8BA', '週次報告の下書き'),
    'finance': ('#68C8FF', '支出分類の下書き'),
    'health': ('#8CDAAB', '生活記録の下書き'),
    'travel': ('#8AB8FF', '旅程案の下書き'),
    'beauty': ('#EBA8D3', 'ケア手順の下書き'),
    'cooking': ('#FFBD87', '献立案の下書き'),
    'education': ('#C6B3FF', '復習計画の下書き'),
    'career': ('#F1CF8A', '面談メモの下書き'),
    'lifestyle': ('#E8AFC4', '家事手順の下書き'),
    'technology': ('#8ED8E2', '設定手順の下書き'),
}
CHECKS = ('数字・根拠', '日付・固有名詞', '断定的な表現')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate():
    assert len(GENRES) == 10 and END - START == 87
    assert len(CHECKS) == 3 and CAPTION_SAFE_Y > 1400
    assert all(c.startswith('#') and len(c) == 7 and label for c, label in GENRES.values())
    assert 'PUBLICATION_NOT_APPROVED' in POLICY
    return True


def make_overlay(stage, genre='ai_work'):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    validate()
    if stage not in (0, 1, 2) or genre not in GENRES:
        raise ValueError('invalid stage or genre')
    accent, topic = GENRES[genre]
    image = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((94, 350, 960, 1410), radius=42, fill=(0, 0, 0, 110))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(13)))
    d = ImageDraw.Draw(image)
    font = lambda n, bold=False: ImageFont.truetype(BOLD if bold else FONT, n)
    d.rounded_rectangle((83, 338, 949, 1400), radius=40, fill='#F5F9FC', outline='#A8C5D1', width=3)
    d.rounded_rectangle((83, 338, 949, 452), radius=40, fill='#102C40')
    d.rectangle((83, 397, 949, 452), fill='#102C40')
    d.text((128, 368), 'HUMAN REVIEW  /  05', font=font(32, True), fill='#DDF7F5')
    d.rounded_rectangle((722, 359, 903, 426), radius=23, fill='#B73F46')
    d.text((742, 371), '未承認', font=font(35, True), fill='#FFFFFF')
    d.text((126, 512), '公開前の3つの確認', font=font(55, True), fill='#142E40')
    d.text((128, 593), topic, font=font(32), fill='#526A79')
    for i, name in enumerate(CHECKS):
        y = 695 + i * 167
        active = i == stage
        d.rounded_rectangle((126, y, 911, y + 132), radius=20,
                            fill='#E1F6F2' if active else '#E8EEF2',
                            outline=accent if active else '#C9D8E0', width=5 if active else 2)
        d.rounded_rectangle((151, y + 33, 214, y + 98), radius=16,
                            fill=accent if active else '#CBD7DE')
        d.text((163, y + 42), f'{i+1:02}', font=font(29, True), fill='#102C40')
        d.text((240, y + 39), name, font=font(40, True), fill='#183347')
        state = '確認対象' if active else '未確認'
        d.rounded_rectangle((700, y + 37, 878, y + 98), radius=19,
                            fill='#174A54' if active else '#D3DEE5')
        d.text((716, y + 49), state, font=font(29, True),
               fill='#FFFFFF' if active else '#465F6D')
    d.rounded_rectangle((125, 1255, 912, 1354), radius=19, fill='#FDE7E5')
    d.text((174, 1277), '確認完了まで投稿しない', font=font(33, True), fill='#A83239')
    # Hard alpha mask: original Japanese burned subtitles and footer are untouched.
    image.paste((0, 0, 0, 0), (0, CAPTION_SAFE_Y, WIDTH, HEIGHT))
    return image


def render(source, output, genre='ai_work', expected_sha=None):
    validate()
    source, output = Path(source), Path(output)
    if expected_sha and sha256(source) != expected_sha:
        raise RuntimeError('SOURCE_SHA_MISMATCH')
    output.parent.mkdir(parents=True, exist_ok=True)
    overlays = []
    for stage in range(3):
        path = output.parent / f'cycle927_stage{stage}.png'
        make_overlay(stage, genre).save(path)
        overlays.append(path)
    filters = ("[0:v][1:v]overlay=0:0:enable='between(n,348,376)':format=auto[v1];"
               "[v1][2:v]overlay=0:0:enable='between(n,377,405)':format=auto[v2];"
               "[v2][3:v]overlay=0:0:enable='between(n,406,434)':format=auto[v]")
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source)]
    for path in overlays:
        cmd += ['-loop', '1', '-framerate', str(FPS), '-i', str(path)]
    cmd += ['-filter_complex', filters, '-map', '[v]', '-map', '0:a:0',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-c:a', 'copy', '-frames:v', '691', '-movflags', '+faststart', str(output)]
    subprocess.run(cmd, check=True, timeout=240)
    return {'source_sha256': sha256(source), 'output_sha256': sha256(output),
            'changed_frames': END-START, 'genre': genre, 'policy': POLICY}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', choices=list(GENRES), default='ai_work')
    p.add_argument('--expected-source-sha')
    p.add_argument('--report')
    a = p.parse_args()
    r = render(a.source, a.output, a.genre, a.expected_source_sha)
    if a.report:
        Path(a.report).write_text(json.dumps(r, ensure_ascii=False, indent=2))
    print(json.dumps(r, ensure_ascii=False))

if __name__ == '__main__':
    main()
