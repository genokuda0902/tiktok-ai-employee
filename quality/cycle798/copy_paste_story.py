"""Original, review-only animated copy→paste proof. No third-party media.

The 10-genre renderer consumes data labels and numbers; this particular demo
uses synthetic monthly sales, not a real business performance claim.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, FRAMES = 1080, 1920, 30, 72
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def validate(config):
    if config.get('mode') != 'review_only':
        raise ValueError('Only review_only allowed')
    if any(config.get(k) is not False for k in ('rights_reviewed', 'employee_approved', 'publication_approved')):
        raise ValueError('Fail closed: rights/employee/publication approval is not granted')
    rows = config.get('rows', [])
    if not 2 <= len(rows) <= 5 or not all(isinstance(x.get('value'), int) and x['value'] >= 0 for x in rows):
        raise ValueError('Use 2–5 nonnegative integer rows')
    if sum(x['value'] for x in rows) != config['total']:
        raise ValueError('Total does not match rows')
    if len(config.get('genres', [])) != 10:
        raise ValueError('Expected 10 shared genres')
    for key in ('title', 'source_label', 'destination_label', 'notice'):
        if not config.get(key):
            raise ValueError(f'Missing {key}')
    return True


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def rounded(draw, box, fill, radius=28, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, s, size, fill, bold=False, anchor=None):
    draw.text(xy, s, font=font(size, bold), fill=fill, anchor=anchor, stroke_width=0)


def gradient():
    im = Image.new('RGB', (W, H))
    p = im.load()
    for y in range(H):
        a = y / H
        r = int(7 + 4*a)
        g = int(18 + 15*a)
        b = int(34 + 17*a)
        for x in range(W):
            p[x,y] = (r,g,b)
    return im


def geometry():
    return {'title': (76, 265, 1004, 385),
            'source': (80, 465, 1000, 860),
            'destination': (80, 1020, 1000, 1515),
            'notice': (80, 1580, 1000, 1640)}


def make_frame(index, config, background=None):
    validate(config)
    if not 0 <= index < FRAMES:
        raise ValueError('frame index out of range')
    im = (background or gradient()).copy()
    d = ImageDraw.Draw(im)
    t = index / FPS
    teal, white, pale, muted = '#28dfc8', '#f5fbff', '#c6dce7', '#8ba5b9'
    # Background editorial grid: noncritical and fully original.
    for x in range(80, 1000, 80):
        d.line((x, 220, x, 1670), fill='#163047', width=1)
    for y in range(240, 1650, 100):
        d.line((70, y, 1010, y), fill='#142b41', width=1)
    rounded(d, (80, 150, 396, 206), '#113c4b', 20, '#248f8b', 2)
    text(d, (101, 159), 'AI時短ラボ / DEMO', 28, teal, True)
    text(d, (80, 264), config['title'], 55, white, True)
    text(d, (82, 346), 'COPY  →  PASTE  →  CHECK', 27, teal, True)
    # Upper source card: legible synthetic table, not screenshots.
    rounded(d, (80, 465, 1000, 860), '#132a40', 34, '#3c6b80', 3)
    rounded(d, (80, 465, 1000, 542), '#21475a', 32)
    text(d, (113, 480), '① ' + config['source_label'], 37, white, True)
    text(d, (125, 560), '月', 34, muted, True)
    text(d, (675, 560), '金額', 34, muted, True)
    for i, row in enumerate(config['rows']):
        y = 618 + i*55
        if i == min(3, int(t*3.5)) and t < 1.0:
            rounded(d, (111, y-5, 962, y+51), '#204f5c', 10)
        text(d, (131, y), str(row['label']), 37, pale, True)
        text(d, (921, y), f"{row['value']:,} 円", 37, white, True, anchor='ra')
    # Animated transfer: a central moving arrow and step marker.
    pulse = 0.5 + 0.5*math.sin(index*0.21)
    cx = 540
    arrow_y = int(917 + (min(1.0, max(0.0, (t-.5)/.7)) * 40))
    d.rounded_rectangle((365, 900, 715, 985), radius=27, fill='#164654', outline=teal, width=3)
    text(d, (540, 913), 'コピー → 貼り付け', 33, white, True, 'ma')
    d.polygon([(cx-22,arrow_y+33),(cx+22,arrow_y+33),(cx,arrow_y+54)], fill=(int(28+20*pulse), 224, 205))
    # Lower spreadsheet card: row-by-row appearance, explicit demo status.
    rounded(d, (80, 1020, 1000, 1515), '#f6fbff', 32, '#2bc8b4', 4)
    rounded(d, (80, 1020, 1000, 1100), '#1a6e61', 28)
    text(d, (110, 1033), '② ' + config['destination_label'], 38, white, True)
    d.rectangle((114, 1134, 966, 1193), fill='#d8e9f0')
    text(d, (145, 1141), '月', 34, '#203c52', True)
    text(d, (650, 1141), '売上（円）', 34, '#203c52', True)
    visible = max(0, min(len(config['rows']), int((t - .75) / .28) + 1))
    for i, row in enumerate(config['rows']):
        y = 1210 + i*59
        fill = '#d5fff3' if i == visible-1 else ('#e8f3f9' if i%2 == 0 else '#ffffff')
        d.rectangle((115, y, 965, y+58), fill=fill)
        if i < visible:
            text(d, (145, y+5), str(row['label']), 37, '#173b50', True)
            text(d, (920, y+5), f"{row['value']:,}", 37, '#0d665a', True, 'ra')
        else:
            text(d, (145, y+6), '—', 33, '#a8c3ce')
    if visible == len(config['rows']):
        rounded(d, (594, 1460, 960, 1503), '#0e675a', 13)
        text(d, (942, 1464), f"合計 {config['total']:,} 円", 26, white, True, 'ra')
    text(d, (80, 1576), config['notice'], 27, '#a6c3d2')
    return im


def render_segment(config, output):
    validate(config)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    bg = gradient()
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
           '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
           '-c:v','libx264','-preset','ultrafast','-crf','21',
           '-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):
            p.stdin.write(make_frame(i, config, bg).tobytes())
        p.stdin.close()
        err = p.stderr.read().decode(errors='replace')
        rc = p.wait()
        if rc:
            raise RuntimeError(f'ffmpeg exit {rc}: {err[-1500:]}')
    finally:
        if p.poll() is None:
            p.kill()
    return output


def splice(source, segment, output):
    # Replace exact source frames 348..419, preserving all audio packets.
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(segment),
           '-filter_complex',
           '[0:v]trim=start_frame=0:end_frame=348,setpts=PTS-STARTPTS[v0];'
           '[1:v]setpts=PTS-STARTPTS[v1];'
           '[0:v]trim=start_frame=420:end_frame=714,setpts=PTS-STARTPTS[v2];'
           '[v0][v1][v2]concat=n=3:v=1:a=0[v];[v]fps=30,setpts=N/(30*TB)[vout]',
           '-map','[vout]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
           '-crf','20','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
           str(output)]
    subprocess.run(cmd,check=True)


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--config',required=True)
    a.add_argument('--segment',required=True)
    a.add_argument('--source')
    a.add_argument('--output')
    args = a.parse_args()
    config = json.loads(Path(args.config).read_text(encoding='utf-8'))
    render_segment(config,args.segment)
    if args.source:
        if not args.output:
            a.error('--output required with --source')
        splice(args.source,args.segment,args.output)

if __name__ == '__main__':
    main()
