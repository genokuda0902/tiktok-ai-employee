"""cycle818: Japanese-first editorial labels on review-only 8-scene video.

Source video is inherited and remains private. No posting, downloads or paid APIs.
The synthetic mode is for CI only, and never claims Japanese narration.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
SCENE_TITLES = (
    '問いを立てる', '目標を決める', '現状を数字で見る', '優先順位を決める',
    '原因を深掘りする', '今日の行動を決める', '結果を振り返る', '成果の変化を見る',
)
GENRE_ACCENTS = {
    'ai_work': '#73CBFF', 'beauty': '#FF9EC4', 'love_psychology': '#C3A2FF',
    'money_saving': '#FFD475', 'sales_business': '#5DE7C4',
    'career': '#86B7FF', 'health_life': '#B6E984',
    'science': '#8DD9FF', 'travel_food': '#FFBB8C',
    'product_life': '#D8B0FF',
}
GENRE_LABELS = {
    'ai_work': 'AI活用', 'beauty': '美容', 'love_psychology': '恋愛心理',
    'money_saving': '節約', 'sales_business': '営業・仕事術',
    'career': 'キャリア', 'health_life': '健康・暮らし',
    'science': '科学', 'travel_food': '旅行・グルメ',
    'product_life': '暮らしの便利術',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def check_config(genre: str):
    if genre not in GENRE_ACCENTS or genre not in GENRE_LABELS:
        raise ValueError('Unknown genre: ' + genre)
    if len(SCENE_TITLES) != 8 or len(GENRE_ACCENTS) != 10:
        raise ValueError('Invalid 8-scene / 10-genre contract')

def overlay_image(index: int, genre: str, font_path: str = FONT) -> Image.Image:
    check_config(genre)
    if index not in range(8):
        raise ValueError('Scene must be 0..7')
    canvas = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    bold = ImageFont.truetype(font_path, 31)
    small = ImageFont.truetype(font_path, 24)
    title_font = ImageFont.truetype(font_path, 35)
    accent = GENRE_ACCENTS[genre]
    # Fully opaque replacements avoid inherited English ghosting.
    d.rounded_rectangle((116, 157, 966, 218), radius=26, fill='#173a4c')
    d.text((146, 168), f'{GENRE_LABELS[genre]}  /  実践ノート', font=bold, fill='#ffffff')
    d.text((852, 169), f'{index+1:02}/08', font=bold, fill=accent)
    # Scene title: a consistent intentional pill rather than a hard-edged patch.
    d.rounded_rectangle((290, 315, 790, 379), radius=28, fill='#071c2b')
    d.text((540, 346), SCENE_TITLES[index], font=title_font, anchor='mm', fill=accent)
    # Remove internal English production/debug metadata from the actual footage.
    # This is a review-only replacement, not a claim of publication approval.
    d.rounded_rectangle((114, 1586, 704, 1693), radius=15, fill='#061c2c')
    d.text((135, 1597), '社内レビュー用｜投稿禁止', font=bold, fill=accent)
    d.text((135, 1647), '※ 数値・画面は説明用の架空例です', font=small, fill='#c7d5e0')
    return canvas

def probe(path: Path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                        '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def render(source: Path, output: Path, genre: str = 'sales_business',
           synthetic_source: bool = False, font_path: str = FONT):
    check_config(genre)
    if not source.is_file():
        raise FileNotFoundError(source)
    info = probe(source)
    vs = next(s for s in info['streams'] if s['codec_type'] == 'video')
    au = [s for s in info['streams'] if s['codec_type'] == 'audio']
    if (vs['width'], vs['height']) != (1080, 1920) or not au:
        raise ValueError('Expected 1080x1920 video with audio')
    if vs.get('avg_frame_rate') != '30/1':
        raise ValueError('Expected 30fps source')
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.parent / 'overlays'; temp.mkdir(exist_ok=True)
    for i in range(8):
        overlay_image(i, genre, font_path).save(temp / f'overlay_{i:02}.png')
    overlay_movie = output.parent / 'overlay818.mov'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-framerate', '1/3', '-start_number', '0', '-i', str(temp / 'overlay_%02d.png'),
        '-vf', 'fps=30', '-t', str(718 / FPS), '-c:v', 'qtrle', '-pix_fmt', 'argb',
        str(overlay_movie)], check=True)
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', str(source), '-i', str(overlay_movie),
        '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]',
        '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
        '-crf', '21', '-threads', '2', '-pix_fmt', 'yuv420p',
        '-c:a', 'copy', '-movflags', '+faststart', str(output)], check=True)
    q = probe(output)
    outv = next(s for s in q['streams'] if s['codec_type'] == 'video')
    report = {
        'cycle': 818, 'genre': genre, 'scene_count': 8, 'genre_count': 10,
        'width': outv['width'], 'height': outv['height'],
        'synthetic_source': synthetic_source,
        'japanese_voice_content_verified': False,
        'word_level_caption_alignment_verified': False,
        'asset_rights_verified': False, 'phone_playback_verified': False,
        'publication_approved': False, 'auto_post': False,
        'change': 'Japanese scene headings and review footer; audio stream copied',
    }
    (output.parent / 'qa818.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    return report

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--source', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    a.add_argument('--genre', default='sales_business', choices=sorted(GENRE_ACCENTS))
    a.add_argument('--synthetic-source', action='store_true')
    a.add_argument('--font', default=FONT)
    opts = a.parse_args()
    print(json.dumps(render(opts.source, opts.output, opts.genre, opts.synthetic_source, opts.font), ensure_ascii=False))
