"""Review-only Writer template-save GUI clip; portable 10-genre safe compositor.

Reimplementation, not v33. All inputs stay local; no posting, network or approval.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cycle833.focal_layout import GENRES, FRAMES

FPS, WIDTH, HEIGHT = 30, 1080, 1920
BOX = (62, 390, 1018, 1390)
CAPTION_TOP = 1452
CROP = (240, 0, 900, 610)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def window(genre: str, scene: int, box=BOX):
    if genre not in GENRES or not isinstance(scene, int) or scene not in range(len(FRAMES)):
        raise ValueError('Unsupported genre or scene')
    x, y, r, b = box
    if not (0 <= x < r <= WIDTH and 0 <= y < b < 1400 < CAPTION_TOP):
        raise ValueError('Protected caption/CTA zone overlap')
    start = sum(FRAMES[:scene])
    return start, start + FRAMES[scene]

def validate_manifest(m: dict):
    if not isinstance(m, dict):
        raise ValueError('Missing provenance manifest')
    kind = m.get('source_kind')
    app = {'local_gui_capture':'LibreOffice Writer',
           'synthetic_test_pattern':'synthetic_ffmpeg_fixture'}.get(kind)
    required = {'data_classification':'fictional','contains_personal_data':False,
                'review_only':True,'publication_approved':False,'application':app}
    if app is None or any(m.get(k) != v for k,v in required.items()):
        raise ValueError('Only fictional, local or synthetic, review-only footage is eligible')

def duration(path: Path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error',
        '-show_entries', 'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', str(path)], text=True).strip())

def build_command(source: Path, capture: Path, output: Path, manifest: dict,
                  genre='ai_work', scene=6, capture_start=.55, font=FONT):
    start, end = window(genre, scene)
    validate_manifest(manifest)
    source, capture, output = map(Path, (source, capture, output))
    if not source.is_file() or not capture.is_file():
        raise FileNotFoundError('Missing source or local Writer capture')
    if output.resolve() in (source.resolve(), capture.resolve()):
        raise ValueError('Refusing to overwrite input')
    sec = (end - start) / FPS
    if capture_start < 0 or duration(capture) + .02 < capture_start + sec:
        raise ValueError('Capture is too short')
    l,t,r,b = BOX
    crop_x,crop_y,crop_w,crop_h = CROP
    vf = (
        f'[1:v]trim=start={capture_start:.6f}:duration={sec:.6f},setpts=PTS-STARTPTS,'
        f'crop={crop_w}:{crop_h}:{crop_x}:{crop_y},scale=870:-2:flags=lanczos,'
        f'pad={r-l}:{b-t}:43:192:color=0x092633,'
        f"drawtext=fontfile={font}:text='指示テンプレートを実際に保存':"
        'fontsize=41:fontcolor=white:x=(w-text_w)/2:y=65,'
        f"drawtext=fontfile={font}:text='{('実際のWriter操作 ・ 架空データ' if manifest['source_kind']=='local_gui_capture' else '合成CI素材 ・ 公開不可')}':"
        'fontsize=27:fontcolor=0x9CF0DC:x=(w-text_w)/2:y=910,'
        f'format=rgba,fade=t=in:st=0:d=0.15:alpha=1,'
        f'fade=t=out:st={sec-.18:.6f}:d=0.18:alpha=1,'
        f'setpts=PTS+{start/FPS:.6f}/TB[clip];'
        f'[0:v][clip]overlay={l}:{t}:eof_action=pass:format=auto,'
        'format=yuv420p[v]'
    )
    return ['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(source),'-i',str(capture),'-filter_complex',vf,
        '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
        '-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
        '-frames:v',str(sum(FRAMES)),'-movflags','+faststart',str(output)]

def render(source, capture, output, manifest, genre='ai_work', scene=6, capture_start=.55):
    out=Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(build_command(source,capture,out,manifest,genre,scene,capture_start),check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','capture','out','manifest'):
        p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--scene',type=int,default=6)
    p.add_argument('--capture-start',type=float,default=.55)
    a=p.parse_args()
    print(render(a.source,a.capture,a.out,json.loads(a.manifest.read_text()),a.genre,a.scene,a.capture_start))
