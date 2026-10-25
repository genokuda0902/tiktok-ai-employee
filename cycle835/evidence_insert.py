"""Review-only real GUI evidence scene, portable across ten editorial genres.

This is a reimplementation, not the original v33 engine. It only combines a
locally captured, fictional-data GUI demonstration with an existing video.
It cannot approve rights, publication or voice quality. No network/API calls.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cycle833.focal_layout import GENRES, FRAMES

FPS = 30
TOTAL_FRAMES = sum(FRAMES)
WIDTH, HEIGHT = 1080, 1920
IMAGE_RECT = (62, 390, 1018, 1390)
CAPTION_TOP = 1452
CTA_TOP = 1400
CROP = (58, 25, 762, 670)  # Genuine Calc toolbar and all A:E data cells.
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def scene_window(genre: str, scene: int, box=IMAGE_RECT):
    if genre not in GENRES:
        raise ValueError('Unsupported genre (fail closed)')
    if not isinstance(scene, int) or not 0 <= scene < len(FRAMES):
        raise ValueError('Invalid scene')
    l, t, r, b = box
    if not (0 <= l < r <= WIDTH and 0 <= t < b < CTA_TOP and b < CAPTION_TOP):
        raise ValueError('Would obscure the caption or CTA safe zone')
    begin = sum(FRAMES[:scene])
    return begin, begin + FRAMES[scene]

def validate_manifest(manifest: dict) -> None:
    """Fail closed: fictional captures only; never infer publication approval."""
    if not isinstance(manifest, dict):
        raise ValueError('Missing provenance manifest')
    required = {
        'data_classification': 'fictional',
        'review_only': True,
        'publication_approved': False,
    }
    if manifest.get('source_kind') not in ('local_gui_capture', 'synthetic_test_pattern'):
        raise ValueError('Unapproved source kind')
    if any(manifest.get(key) != value for key, value in required.items()):
        raise ValueError('Capture not eligible for local review composition')
    if manifest.get('contains_personal_data') is not False:
        raise ValueError('Personal data must be absent')

def video_duration(path: Path) -> float:
    output = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(path)
    ], text=True)
    return float(output.strip())

def build_command(source: Path, capture: Path, output: Path,
                  genre: str, scene: int, manifest: dict,
                  capture_start: float = 1.0, font: str = FONT):
    start, end = scene_window(genre, scene)
    validate_manifest(manifest)
    source, capture, output = map(Path, (source, capture, output))
    if not source.is_file() or not capture.is_file():
        raise FileNotFoundError('Source video or captured GUI footage missing')
    if output.resolve() in (source.resolve(), capture.resolve()):
        raise ValueError('Cannot overwrite source footage')
    duration = (end - start) / FPS
    if capture_start < 0 or video_duration(capture) < capture_start + duration - .02:
        raise ValueError('GUI footage too short for scene')
    l, t, r, b = IMAGE_RECT
    width, height = r-l, b-t
    crop_x, crop_y, crop_w, crop_h = CROP
    proof_label = ('実際のCalc操作・架空データ' if manifest['source_kind'] == 'local_gui_capture'
                   else '合成テスト素材・公開不可')
    # Crop preserves fictional source values, discrepancy, and corrected result.
    # Outer application margins are removed for mobile legibility.
    vf = (
        f'[1:v]trim=start={capture_start:.6f}:duration={duration:.6f},'
        'setpts=PTS-STARTPTS,'
        f'crop={crop_w}:{crop_h}:{crop_x}:{crop_y},'
        'scale=870:-2:flags=lanczos,'
        f'pad={width}:{height}:43:124:color=0x0a2632,'
        f"drawtext=fontfile={font}:text='元データと照合する':"
        'fontsize=49:fontcolor=white:x=(w-text_w)/2:y=38,'
        f"drawtext=fontfile={font}:text='{proof_label}':"
        'fontsize=28:fontcolor=0xA9F0DF:x=(w-text_w)/2:y=932,'
        'format=rgba,fade=t=in:st=0:d=0.12:alpha=1,'
        f'fade=t=out:st={duration-.15:.6f}:d=0.15:alpha=1,'
        f'setpts=PTS+{start/FPS:.6f}/TB[proof];'
        f'[0:v][proof]overlay={l}:{t}:eof_action=pass:format=auto,'
        'format=yuv420p[v]'
    )
    return ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(source), '-i', str(capture), '-filter_complex', vf,
            '-map', '[v]', '-map', '0:a:0',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
            '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
            '-frames:v', str(TOTAL_FRAMES), '-movflags', '+faststart', str(output)]

def render(source, capture, output, manifest, genre='ai_work', scene=4,
           capture_start=1.0):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_command(Path(source), Path(capture), output, genre, scene,
                        manifest, capture_start)
    subprocess.run(cmd, check=True)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--capture', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--genre', default='ai_work')
    parser.add_argument('--scene', type=int, default=4)
    parser.add_argument('--capture-start', type=float, default=1.0)
    a = parser.parse_args()
    print(render(a.source, a.capture, a.out,
                 json.loads(a.manifest.read_text(encoding='utf-8')),
                 a.genre, a.scene, a.capture_start))
