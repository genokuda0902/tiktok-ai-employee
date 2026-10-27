"""Render scene-only dissolves from prior-cycle local review assets.

Requires Pillow, FFmpeg and local files. Inherited voice reuse rights are
unverified; output is HUMAN_REVIEW only, never automatically posted.
"""
from pathlib import Path
import shutil
import subprocess
from PIL import Image
from scene_transitions import plan, transition_alpha, source_gate, FRAME_COUNT, FPS

ROOT = Path(__file__).resolve().parents[2] / 'cycle884'
PREV = ROOT.parent / 'cycle883'
SRC = PREV / 'assets'
ASSETS = ROOT / 'assets'
WORK = ROOT / 'work'
OUT = ROOT / 'output'
MP4 = OUT / 'cycle884_SCENE_EASE_DISSOLVE_JP_HUMAN_REVIEW.mp4'

def build_timeline():
    source_gate(provenance='prior-cycle locally authored slides and mock Chromium UI')
    for directory in (ASSETS, WORK, OUT):
        directory.mkdir(parents=True, exist_ok=True)
    lines = ['ffconcat version 1.0']
    transitions = []
    for segment in plan():
        if segment.kind == 'still':
            path = SRC / f's{segment.scene:02d}_state{segment.stage:02d}.png'
            if not path.exists():
                raise FileNotFoundError(path)
        else:
            first_path = SRC / f's{segment.scene:02d}_state{segment.stage:02d}.png'
            next_path = SRC / f's{segment.scene+1:02d}_state00.png'
            path = ASSETS / f'transition_s{segment.scene:02d}_{segment.step:02d}.png'
            with Image.open(first_path) as first, Image.open(next_path) as second:
                if first.size != (1080, 1920) or second.size != (1080, 1920):
                    raise ValueError('unexpected source dimensions')
                Image.blend(first.convert('RGB'), second.convert('RGB'),
                            transition_alpha(segment.step)).save(path, compress_level=3)
            transitions.append(path)
        lines.extend([f"file '{path.resolve()}'", f'duration {segment.frames/FPS:.9f}'])
    lines.append(f"file '{(SRC/'s08_state00.png').resolve()}'")
    concat = WORK / 'states_eased.ffconcat'
    concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    shutil.copyfile(PREV/'work/captions.ass', WORK/'captions.ass')
    return concat, transitions

def render():
    concat, transitions = build_timeline()
    audio = SRC / 'voice_japanese_inherited.m4a'
    if not audio.exists():
        raise FileNotFoundError('Japanese narration missing')
    cmd = ['ffmpeg','-y','-hide_banner','-loglevel','error',
           '-f','concat','-safe','0','-i',str(concat),
           '-i',str(audio),
           '-vf',f"fps={FPS},scale=1080:1920:flags=lanczos,format=yuv420p,ass=filename='{WORK/'captions.ass'}'",
           '-map','0:v:0','-map','1:a:0','-frames:v',str(FRAME_COUNT),
           '-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','19',
           '-threads','2','-pix_fmt','yuv420p','-c:a','copy',
           '-movflags','+faststart',str(MP4)]
    subprocess.run(cmd,check=True,timeout=240)
    return MP4, transitions

if __name__ == '__main__':
    print(render()[0])
