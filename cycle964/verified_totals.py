"""cycle964: arithmetic continuity scene for a PRIVATE REVIEW ONLY MP4.

Not original v33. Uses only a synthetic table derived from fictional values
already visible in the user's previous review clip. Keeps the existing
Japanese narration and burned subtitles; does NOT independently ASR-check them.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA = '5df3b08c7ec6d18d3de52616939bc5b36fd1d1f3d790b5caf0e50d5c8cf54c6f'
ROWS = (("4月", 12, 8), ("5月", 16, 9), ("6月", 18, 12))
TOTALS = (46, 29)
FPS = 30
START_FRAME = 348  # 11.600s
SCENE_FRAMES = 87  # 2.900s
W, H = 1080, 1450  # never touch the existing subtitle area y>=1490
GENRE_RULES = {
    'ai_work': 'spreadsheet arithmetic proof',
    'finance': 'source-backed totals with currency labels',
    'history': 'date/source consistency',
    'science': 'unit and experiment consistency',
    'health': 'approved source-backed figures',
    'travel': 'verified itinerary times',
    'food': 'verified quantities and portions',
    'career': 'source-backed application figures',
    'education': 'worked arithmetic examples',
    'lifestyle': 'source-backed before/after values',
}
REVIEWED = frozenset({'ai_work'})
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def arithmetic(rows=ROWS, totals=TOTALS):
    if len(rows) != 3 or any(len(r) != 3 or r[1] < 0 or r[2] < 0 for r in rows):
        raise ValueError('invalid fictional source rows')
    result = (sum(r[1] for r in rows), sum(r[2] for r in rows))
    if tuple(totals) != result:
        raise ValueError(f'inconsistent cross-scene totals: expected {result}, got {totals}')
    return result


def gate(source, genre='ai_work', review_only=True, publish_approved=False):
    if genre not in GENRE_RULES:
        raise ValueError('unknown genre')
    if genre not in REVIEWED:
        raise PermissionError('genre visual and source rights not reviewed')
    if review_only is not True or publish_approved is not False:
        raise PermissionError('manual employee approval required for publication')
    arithmetic()
    if not Path(source).is_file() or digest(source) != SOURCE_SHA:
        raise ValueError('missing private cycle963 source or SHA mismatch')


def font(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else FONT_PATH, size)


def pill(draw, box, color, outline=None, width=2, radius=22):
    draw.rounded_rectangle(box, radius=radius, fill=color, outline=outline, width=width)


def frame(idx):
    """Deterministic visual: inspect -> recompute -> verified totals."""
    if not 0 <= idx < SCENE_FRAMES:
        raise ValueError('frame out of range')
    stage = 0 if idx < 26 else 1 if idx < 60 else 2
    im = Image.new('RGB', (W, H), '#061421')
    d = ImageDraw.Draw(im)
    # Original graphic design, no third-party photos or app UI impersonation.
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(7+3*t), int(24+12*t), int(40+19*t)))
    pill(d, (45, 36, 1035, 1380), '#0b2234', '#247c9a', 3, 36)
    d.text((84, 74), 'AI仕事術 / SOURCE CHECK', font=font(34, True), fill='#9ddff0')
    d.text((84, 149), '合計を、元データで検算', font=font(64, True), fill='white')
    d.text((84, 248), '架空データによる計算例 / 実操作画面ではありません', font=font(27), fill='#a8c5d5')
    # Table header and original rows. Fixed exact values from prior verified proof.
    pill(d, (78, 332, 1002, 775), '#e8f2f6', radius=22)
    pill(d, (94, 348, 986, 422), '#c5e6f2', radius=12)
    for x, text in ((125, '月'), (465, '営業A'), (735, '営業B')):
        d.text((x, 361), text, font=font(35, True), fill='#12324c')
    for j, (month, a, b) in enumerate(ROWS):
        y = 449 + j*89
        if j % 2 == 0:
            d.rounded_rectangle((101, y-6, 978, y+72), radius=9, fill='#d9e9ef')
        d.text((127, y), month, font=font(39), fill='#172e41')
        d.text((489, y), str(a), font=font(41, True), fill='#172e41')
        d.text((765, y), str(b), font=font(41, True), fill='#172e41')
    # Staged arithmetic; final two totals are both exact sums.
    pill(d, (78, 817, 1002, 1227), '#0e3445', '#278ea5', 3, 25)
    if stage == 0:
        d.text((112, 846), 'STEP 1 / 元データを確認', font=font(40, True), fill='#78e5f0')
        d.text((118, 941), '数字の抜け・入力ミスを確認', font=font(44, True), fill='white')
        d.text((118, 1050), '合計欄だけを信用しない', font=font(37), fill='#c7dbe2')
    elif stage == 1:
        d.text((112, 846), 'STEP 2 / 足し算で照合', font=font(40, True), fill='#78e5f0')
        d.text((118, 939), '営業A   12 + 16 + 18 = 46', font=font(43, True), fill='white')
        d.text((118, 1050), '営業B     8 + 9 + 12 = 29', font=font(43, True), fill='white')
    else:
        d.text((112, 846), 'STEP 3 / 計算上の合計を確認', font=font(40, True), fill='#78e5f0')
        pill(d, (119, 936, 955, 1137), '#126350', '#48e5ad', 3, 23)
        d.text((151, 964), '営業A  46   /   営業B  29', font=font(50, True), fill='white')
        d.text((155, 1051), '計算式と一致 ✓', font=font(35, True), fill='#bdf5d8')
    for j in range(3):
        x0=127+j*286
        pill(d,(x0,1265,x0+247,1281),'#2de6d0' if j<=stage else '#2a5262',radius=8)
    d.text((96, 1325), '※ 数値は説明用の架空データ。公開前に内容を人が確認。', font=font(27), fill='#a8c5d5')
    return im


def run(args, stdout=False):
    p=subprocess.run(args, stdout=subprocess.PIPE if stdout else subprocess.DEVNULL,
                     stderr=subprocess.PIPE, check=False, timeout=240)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout if stdout else None


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],True))


def render(source, output, genre='ai_work'):
    gate(source, genre)
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle964_') as td:
        scene=Path(td)/'scene.mp4'
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
             '-s',f'{W}x{H}','-r',str(FPS),'-i','-', '-an','-c:v','libx264','-preset','ultrafast',
             '-crf','17','-pix_fmt','yuv420p',str(scene)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for i in range(SCENE_FRAMES):
                p.stdin.write(frame(i).tobytes())
            p.stdin.close();err=p.stderr.read();rc=p.wait(timeout=120)
            if rc:raise RuntimeError(err.decode(errors='replace')[-1500:])
        finally:
            if p.poll() is None:p.kill()
        # Place only over scene05; protect the existing lower narration captions.
        # Stream-copy original Japanese AAC (no sound recompression).
        filt=f'[1:v]setpts=PTS+{START_FRAME/FPS}/TB[scene];[0:v][scene]overlay=x=0:y=0:enable=\'between(t,{START_FRAME/FPS},{(START_FRAME+SCENE_FRAMES-1)/FPS})\':eof_action=pass[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(scene),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30',
             '-c:a','copy','-movflags','+faststart',str(output)])
    return {'source_sha256':digest(source),'output_sha256':digest(output),
            'changed_scene':'scene05 frames 348..434 (11.6..14.5s)',
            'verified_fictional_totals':arithmetic(),
            'audio':'original Japanese AAC stream copied; no independent ASR',
            'captions':'original burned subtitles below y=1490 protected by overlay bounds',
            'genre':genre,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
    report=render(a.source,a.output,a.genre)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
