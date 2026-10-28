"""Zero-cost, conservative Japanese narration clarity pass for a private review MP4.

Audio only: copy H.264 video (and baked captions) bit-for-bit; no media is
uploaded or posted. Requires installed FFmpeg. Not a substitute for ASR,
listening tests, or source-rights approval.
"""
import argparse
import subprocess
from pathlib import Path

# Frequency (Hz), gentle presence boost (dB). 10 reusable genre profiles.
PROFILES = {
    'ai_productivity': (75, 2800, 1.4),
    'business': (75, 2700, 1.2),
    'finance': (75, 2700, 1.2),
    'education': (70, 2600, 1.3),
    'health': (70, 2500, 1.1),
    'beauty': (80, 3000, 1.2),
    'food': (70, 2900, 1.1),
    'travel': (75, 2900, 1.1),
    'lifestyle': (70, 2800, 1.2),
    'technology': (75, 2800, 1.4),
}

def filter_chain(genre='ai_productivity'):
    if genre not in PROFILES:
        raise ValueError('unrecognized genre; fail closed')
    hp, presence_hz, gain_db = PROFILES[genre]
    if not (60 <= hp <= 100 and 2300 <= presence_hz <= 3300 and 0 < gain_db <= 1.5):
        raise ValueError('unsafe EQ profile')
    # Fixed peak ceiling; no auto makeup gain or loudness maximization.
    return (f'highpass=f={hp},'
            f'equalizer=f={presence_hz}:t=q:w=1.0:g={gain_db:.1f},'
            'lowpass=f=14500,alimiter=limit=0.88:level=0')

def command(src:Path, dst:Path, genre='ai_productivity'):
    if src.resolve() == dst.resolve():
        raise ValueError('must not overwrite source')
    return ['ffmpeg','-hide_banner','-nostdin','-y','-i',str(src),
            '-map','0:v:0','-map','0:a:0',
            '-c:v','copy','-af',filter_chain(genre),
            '-c:a','aac','-b:a','192k','-ar','48000',
            '-movflags','+faststart',str(dst)]

def render(src:Path, dst:Path, genre='ai_productivity'):
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(command(src,dst,genre),check=True)
    return dst

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=list(PROFILES),default='ai_productivity')
    a=p.parse_args()
    print(render(a.source,a.output,a.genre))
