#!/usr/bin/env python3
"""cycle734: self-contained original prompt-entry animation, 10-genre capable.

This is a simulated UI. No third-party logos, reference image copying, private
assets, API calls, or real AI requests. All output requires human review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT, FPS, TOTAL_FRAMES = 1080, 1920, 30, 819
START_FRAME, END_FRAME = 195, 294  # 6.500–9.800 seconds
PHASE_FRAMES = (24, 25, 25, 25)
PALETTES = {
    'ai_work': '#63F2E2', 'beauty': '#FFB8D4',
    'love_psychology': '#FFB4E0', 'saving': '#A6E8B4',
    'sales_business': '#FFD28B', 'career': '#A8C7FF',
    'health': '#A2E5D4', 'science': '#B7B5FF',
    'travel_food': '#FFBF9B', 'product_comparison': '#C6D3FF',
}
FONT_CANDIDATES = (
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
)
CAPTION = ('この表をAIに渡して、', 'グラフを依頼。')


def font(size):
    path = next((p for p in FONT_CANDIDATES if Path(p).exists()), None)
    if not path:
        raise FileNotFoundError('Japanese font missing: install fonts-noto-cjk')
    return ImageFont.truetype(path, size)


def validate(genre):
    if genre not in PALETTES or len(PALETTES) != 10:
        raise ValueError('Unknown genre or incomplete palette')
    if sum(PHASE_FRAMES) != END_FRAME - START_FRAME:
        raise AssertionError('Incorrect scene length')
    if START_FRAME < 0 or END_FRAME > TOTAL_FRAMES:
        raise AssertionError('Scene outside timeline')


def write_fit(d, xy, text, size, max_width, fill):
    f = font(size)
    box = d.textbbox((0, 0), text, font=f)
    if box[2] - box[0] > max_width:
        raise ValueError(f'Text overflow: {text}')
    d.text(xy, text, font=f, fill=fill)


def frame(phase: int, genre: str = 'ai_work') -> Image.Image:
    validate(genre)
    if phase not in range(4):
        raise ValueError('phase must be 0–3')
    accent = PALETTES[genre]
    img = Image.new('RGB', (WIDTH, HEIGHT), '#071B30')
    d = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        k = y / HEIGHT
        d.line((0, y, WIDTH, y), fill=(int(5+13*k), int(22+14*k), int(41+25*k)))
    glow = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    g = ImageDraw.Draw(glow)
    g.ellipse((-260, 70, 690, 1020), fill=(0, 203, 213, 140))
    g.ellipse((460, 390, 1450, 1480), fill=(47, 89, 246, 115))
    img = Image.alpha_composite(img.convert('RGBA'), glow.filter(ImageFilter.GaussianBlur(155)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((64, 90, 775, 160), radius=18, fill='#123B54', outline='#3E7894', width=2)
    write_fit(d, (86, 101), 'AI時短ラボ  /  入力デモ', 35, 650, accent)
    write_fit(d, (67, 205), '日本語で指示するだけ', 59, 900, '#FFFFFF')
    write_fit(d, (68, 299), '架空の売上データを使った操作イメージ', 31, 920, '#C7DCEB')

    # Original desktop UI, not a screenshot of an actual third-party service.
    sh = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((94, 435, 1014, 1197), radius=40, fill=(0,0,0,150))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((70, 408, 1010, 1157), radius=38, fill='#EAF4F8', outline='#77BBD2', width=6)
    d.rounded_rectangle((70, 408, 1010, 494), radius=38, fill='#154B68')
    d.rectangle((70, 458, 1010, 494), fill='#154B68')
    for i, c in enumerate(('#FE8883','#FFD47D','#64D5BC')):
        d.ellipse((104+i*39, 439, 123+i*39, 458), fill=c)
    write_fit(d, (272, 427), 'AIへの指示  /  DEMO', 33, 640, '#FFFFFF')

    # File attachment first, then progressively typed prompt.
    d.rounded_rectangle((120, 528, 960, 643), radius=20,
                        fill='#D7EBF2' if phase == 0 else '#C7F5EB',
                        outline=accent if phase >= 1 else '#8FB5C7', width=4)
    d.rounded_rectangle((148, 552, 199, 613), radius=10, fill='#1B9E88')
    write_fit(d, (160, 561), '表', 28, 38, '#FFFFFF')
    write_fit(d, (225, 542), '売上データ_架空.csv', 37, 670, '#17374B')
    write_fit(d, (225, 596), '添付済み  •  サンプルデータ', 24, 660, '#32677A')

    d.rounded_rectangle((120, 687, 960, 971), radius=24, fill='#FFFFFF', outline='#A6C6D4', width=3)
    write_fit(d, (154, 710), '入力する指示', 30, 650, '#426C82')
    if phase == 0:
        d.rounded_rectangle((154, 778, 164, 846), radius=4, fill='#38BEB6')
        write_fit(d, (184, 774), 'ここに日本語で入力', 40, 710, '#8CA6B5')
    else:
        write_fit(d, (155, 774), 'この売上データを分析して', 42, 760, '#102B3C')
        if phase >= 2:
            write_fit(d, (155, 853), '月別グラフを作成してください', 40, 770, '#102B3C')
        if phase == 1:
            d.rectangle((786, 784, 794, 833), fill='#29B8AC')
        if phase == 2:
            d.rectangle((823, 861, 831, 911), fill='#29B8AC')
    # CTA button is highlighted on phase 3 only; never imply an actual request was sent.
    button = '#00A999' if phase == 3 else '#307D9E'
    d.rounded_rectangle((729, 995, 959, 1100), radius=27, fill=button)
    write_fit(d, (770, 1018), '送信', 37, 145, '#FFFFFF')
    d.line((890, 1049, 935, 1049), fill='#FFFFFF', width=7)
    d.line((920, 1034, 935, 1049, 920, 1064), fill='#FFFFFF', width=7, joint='curve')
    if phase == 3:
        d.rounded_rectangle((154, 1004, 697, 1091), radius=20, fill='#CFF6EC')
        write_fit(d, (175, 1020), '送信する操作イメージ', 30, 510, '#14675C')
    else:
        write_fit(d, (157, 1025), f'STEP {phase+1} / 4', 30, 400, '#50798B')

    # Caption layer: fully opaque and consistent with the inherited spoken line.
    d.rounded_rectangle((69, 1240, 1011, 1532), radius=32, fill='#07192B', outline=accent, width=5)
    d.rounded_rectangle((97, 1274, 109, 1497), radius=6, fill=accent)
    write_fit(d, (148, 1294), CAPTION[0], 66, 820, '#FFFFFF')
    write_fit(d, (148, 1410), CAPTION[1], 65, 820, accent)
    d.rounded_rectangle((72, 1580, 1010, 1596), radius=7, fill='#244C67')
    d.rounded_rectangle((72, 1580, 72+int(938*(phase+1)/4), 1596), radius=7, fill=accent)
    write_fit(d, (76, 1661), '※ 操作イメージ / 架空データ / 社員承認前', 30, 935, '#C2D9E4')
    return img.convert('RGB')


def run(cmd, timeout=300):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, timeout=timeout)


def probe(path, count_frames=False):
    return json.loads(run(['ffprobe', '-v', 'error'] + (['-count_frames'] if count_frames else []) +
                          ['-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)


def make_scene(directory: Path, genre='ai_work') -> Path:
    validate(genre)
    directory.mkdir(parents=True, exist_ok=True)
    clips = []
    for phase, count in enumerate(PHASE_FRAMES):
        png = directory / f'prompt_phase{phase}.png'
        frame(phase, genre).save(png)
        clip = directory / f'prompt_phase{phase}.mp4'
        # Exactly count frames per phase; slight motion gives a living UI.
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-loop', '1',
             '-framerate', str(FPS), '-i', str(png), '-vf',
             f"zoompan=z='min(zoom+0.00025,1.018)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={count}:s=1080x1920:fps=30,format=yuv420p",
             '-frames:v', str(count), '-an', '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '21', str(clip)], timeout=180)
        clips.append(clip)
    playlist = directory / 'concat.txt'
    playlist.write_text(''.join("file '" + str(p.resolve()) + "'\n" for p in clips))
    out = directory / 'cycle734_scene.mp4'
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0',
         '-i', str(playlist), '-c', 'copy', str(out)])
    actual = next(s for s in probe(out, True)['streams'] if s['codec_type'] == 'video')
    if int(actual['nb_read_frames']) != END_FRAME-START_FRAME:
        raise AssertionError('Scene frame count mismatch')
    return out


def render(source: Path, output: Path, genre='ai_work') -> dict:
    validate(genre)
    if not source.exists():
        raise FileNotFoundError(source)
    meta = probe(source, True)
    vs = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    if (int(vs['width']), int(vs['height']), int(vs['nb_read_frames'])) != (WIDTH, HEIGHT, TOTAL_FRAMES):
        raise ValueError('Expected a 1080x1920, 819-frame baseline')
    if not any(s['codec_type'] == 'audio' for s in meta['streams']):
        raise ValueError('Baseline must include approved-to-reuse narration')
    output.parent.mkdir(parents=True, exist_ok=True)
    work = output.parent / '_work'
    scene = make_scene(work, genre)
    video = work / 'silent.mp4'
    fc = (f'[0:v]trim=start_frame=0:end_frame={START_FRAME},setpts=PTS-STARTPTS[a];'
          f'[1:v]setpts=PTS-STARTPTS[b];'
          f'[0:v]trim=start_frame={END_FRAME}:end_frame={TOTAL_FRAMES},setpts=PTS-STARTPTS[c];'
          '[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[out]')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
         '-i', str(scene), '-filter_complex', fc, '-map', '[out]', '-an',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
         '-pix_fmt', 'yuv420p', '-frames:v', str(TOTAL_FRAMES), str(video)])
    # Preserve original compressed Japanese narration exactly; no TTS changes.
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(video),
         '-i', str(source), '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy',
         '-movflags', '+faststart', str(output)])
    meta_out = probe(output, True)
    vo = next(s for s in meta_out['streams'] if s['codec_type'] == 'video')
    if int(vo['nb_read_frames']) != TOTAL_FRAMES:
        raise AssertionError('Lost frame during concatenation')
    return {'output': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'frames': TOTAL_FRAMES, 'changed_frames': [START_FRAME, END_FRAME-1],
            'duration': float(meta_out['format']['duration']), 'genres': len(PALETTES),
            'human_review_required': True, 'publication_approved': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--genre', default='ai_work')
    p.add_argument('--scene-only', action='store_true')
    a = p.parse_args()
    if a.scene_only:
        scene = make_scene(a.output.parent, a.genre)
        if scene != a.output:
            a.output.write_bytes(scene.read_bytes())
        print(json.dumps({'scene': str(a.output), 'frames': END_FRAME-START_FRAME, 'review_only': True}))
    else:
        if a.source is None:
            p.error('--source required for full render')
        print(json.dumps(render(a.source, a.output, a.genre), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
