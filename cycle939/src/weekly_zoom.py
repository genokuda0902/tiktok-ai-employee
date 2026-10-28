"""cycle939: legible 3-beat weekly task close-up for a private review MP4.

Zero external images, synthetic on-screen example only. Never uploads or posts.
The existing H264 video is re-encoded; original AAC bitstream is remuxed unchanged.
"""
from __future__ import annotations
import argparse
from pathlib import Path

FPS = 30
START_FRAME = 87
FRAME_COUNT = 87
CANVAS = (1080, 1920)
WORK_BAND = (45, 385, 920, 1390)  # only edits inside this band
SUBTITLE_TOP = 1400
GENRES = {
    'ai_productivity': ('#30d9ca', '週次報告'),
    'business': ('#4db2ff', '定例報告'),
    'finance': ('#65d2ac', '経費集計'),
    'education': ('#f4bd64', '授業準備'),
    'health': ('#7ed4b0', '記録整理'),
    'beauty': ('#f49bbd', '予約管理'),
    'food': ('#f6ad69', '発注管理'),
    'travel': ('#6ec5e8', '旅程整理'),
    'lifestyle': ('#b4a5ff', '家事リスト'),
    'technology': ('#4cdbd5', '作業ログ'),
}

def stage_for_frame(i: int) -> int:
    if not 0 <= i < FRAME_COUNT:
        raise ValueError('frame outside scene02')
    return min(2, i // 29)

def safe_region() -> bool:
    return WORK_BAND[3] < SUBTITLE_TOP and WORK_BAND[1] > 350

def color_to_rgb(color):
    return tuple(int(color[j:j+2], 16) for j in (1, 3, 5))

def _fonts():
    from PIL import ImageFont
    path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    regular = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    if not Path(path).exists():
        raise FileNotFoundError('Japanese Noto CJK font not installed')
    return {n: ImageFont.truetype(path if bold else regular, size) for n, (size, bold) in {
        'eyebrow': (28, False), 'header': (48, True), 'tab': (30, True),
        'big': (72, True), 'body': (38, False), 'foot': (27, False),
        'number': (56, True), 'small': (33, True),
    }.items()}

def render_frame(image, index: int, genre='ai_productivity'):
    """Render a sharp, full-resolution editorial inset without touching subtitles."""
    from PIL import Image, ImageDraw
    if genre not in GENRES:
        raise ValueError('unknown genre; fail closed')
    if image.size != CANVAS:
        raise ValueError('requires exact 1080x1920 input')
    if not safe_region():
        raise RuntimeError('subtitle region not protected')
    stage = stage_for_frame(index)
    accent, task = GENRES[genre]
    rgb = color_to_rgb(accent)
    f = _fonts()
    x0, y0, x1, y1 = WORK_BAND
    roi = image.crop(WORK_BAND).convert('RGBA')
    lay = Image.new('RGBA', roi.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    W, H = roi.size
    d.rounded_rectangle((0, 0, W-1, H-1), radius=36,
                        fill=(2, 24, 46, 247), outline=rgb+(255,), width=3)
    d.text((48, 38), 'WORKFLOW / 02   •   見やすい拡大表示', font=f['eyebrow'], fill=rgb)
    d.text((48, 95), '繰り返す作業を見つける', font=f['header'], fill='white')
    for j in range(3):
        left = 47 + j * 258
        selected = j == stage
        fill = rgb + (255,) if selected else (30, 59, 82, 255)
        d.rounded_rectangle((left, 192, left+230, 263), radius=18, fill=fill)
        d.text((left+48, 202), f'第{j+1}週', font=f['tab'],
               fill=(2, 30, 45, 255) if selected else (217, 230, 242, 255))
    d.rounded_rectangle((48, 305, W-49, 666), radius=27, fill=(244, 249, 251, 255))
    d.rounded_rectangle((78, 335, 265, 396), radius=17, fill=rgb+(255,))
    d.text((105, 338), f'第{stage+1}週', font=f['tab'], fill=(5, 30, 46, 255))
    d.text((79, 415), task, font=f['big'], fill=(7, 33, 53, 255))
    d.line((80, 535, W-90, 535), fill=(186, 209, 217, 255), width=3)
    d.text((80, 561), '同じ仕事を毎週くり返す', font=f['body'], fill=(41, 70, 86, 255))
    d.text((54, 705), '共通作業を1つ選ぶ', font=f['small'], fill=(235, 247, 249, 255))
    d.rounded_rectangle((52, 766, W-53, 824), radius=18, fill=(17, 67, 76, 255))
    d.rounded_rectangle((52, 766, 52+int((W-105)*(stage+1)/3), 824), radius=18,
                        fill=rgb+(255,))
    d.text((W-185, 706), f'{stage+1} / 3', font=f['small'], fill=rgb)
    d.text((53, 837), '※架空の例・公開前に人が確認', font=f['foot'], fill=(168, 195, 206, 255))
    d.rounded_rectangle((49, 894, W-50, 978), radius=18, fill=(9, 53, 70, 255))
    d.text((72, 907), 'NEXT  →  完成形の見本を用意', font=f['small'], fill=(239, 250, 252, 255))
    opacity = min(1.0, index / 7.0, (FRAME_COUNT-1-index)/7.0)
    if opacity < 1:
        lay.putalpha(lay.getchannel('A').point(lambda a: round(a*opacity)))
    out_roi = Image.alpha_composite(roi, lay).convert('RGB')
    out = image.copy().convert('RGB')
    out.paste(out_roi, (x0, y0))
    return out

def render_video(src: Path, out: Path, genre='ai_productivity'):
    import cv2
    import subprocess
    import numpy as np
    from PIL import Image
    if not src.is_file():
        raise FileNotFoundError(src)
    if src.resolve() == out.resolve():
        raise ValueError('source overwrite forbidden')
    if genre not in GENRES:
        raise ValueError('unknown genre')
    out.parent.mkdir(parents=True, exist_ok=True)
    video_only = out.with_suffix('.silent.mp4')
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise RuntimeError('cannot decode source')
    if (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) != CANVAS:
        raise RuntimeError('unexpected resolution')
    args = ['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
            '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
            '-an','-c:v','libx264','-preset','veryfast','-crf','18',
            '-pix_fmt','yuv420p','-movflags','+faststart',str(video_only)]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    frames = 0
    try:
        while True:
            ok, bgr = cap.read()
            if not ok:
                break
            if START_FRAME <= frames < START_FRAME+FRAME_COUNT:
                rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                img = render_frame(Image.fromarray(rgb), frames-START_FRAME, genre)
                bgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            proc.stdin.write(bgr.tobytes())
            frames += 1
    finally:
        cap.release()
        if proc.stdin:
            proc.stdin.close()
    error = proc.stderr.read().decode('utf-8', errors='replace')
    if proc.wait() != 0:
        raise RuntimeError('ffmpeg encode failed: '+error[-1500:])
    if frames != 691:
        raise RuntimeError(f'expected 691 frames, got {frames}')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
                    '-i',str(video_only),'-i',str(src),'-map','0:v:0','-map','1:a:0',
                    '-c:v','copy','-c:a','copy','-movflags','+faststart',str(out)],check=True)
    video_only.unlink()
    return frames

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=tuple(GENRES),default='ai_productivity')
    a = p.parse_args()
    print('frames',render_video(a.source,a.output,a.genre))
