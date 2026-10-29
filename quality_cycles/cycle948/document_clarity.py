"""Offline scene-limited document clarity enhancement. Human review only."""
from dataclasses import dataclass
from pathlib import Path
import subprocess

GENRE_STRENGTH = {
    'ai_productivity': 0.85, 'business': 0.70, 'education': 0.80,
    'finance': 0.65, 'technology': 0.80, 'lifestyle': 0.50,
    'health': 0.55, 'travel': 0.45, 'food': 0.40, 'entertainment': 0.55,
}

@dataclass(frozen=True)
class FocusArea:
    x: int = 108
    y: int = 355
    width: int = 828
    height: int = 794
    start: float = 5.80
    end: float = 8.70

    def validate(self):
        if not (0 <= self.x and 0 <= self.y and self.x + self.width <= 1080):
            raise ValueError('region outside frame')
        if not (self.y + self.height <= 1250):
            raise ValueError('must not touch subtitles or footer')
        if not (0 <= self.start < self.end <= 23.0334):
            raise ValueError('invalid time range')
        if self.width % 2 or self.height % 2:
            raise ValueError('crop must have even dimensions')

def filter_complex(genre: str = 'ai_productivity', area: FocusArea = FocusArea()) -> str:
    area.validate()
    if genre not in GENRE_STRENGTH:
        raise ValueError('unsupported genre')
    amount = GENRE_STRENGTH[genre]
    return (
        '[0:v]split=2[base][region];'
        f'[region]crop={area.width}:{area.height}:{area.x}:{area.y},'
        f'unsharp=5:5:{amount:.2f}:5:5:0[clear];'
        f"[base][clear]overlay={area.x}:{area.y}:enable='between(t,{area.start:.2f},{area.end:.2f})':shortest=1[v]"
    )

def render(source: Path, destination: Path, genre: str = 'ai_productivity'):
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-filter_complex', filter_complex(genre), '-map', '[v]', '-map', '0:a:0',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p',
        '-r', '30', '-fps_mode', 'cfr', '-frames:v', '691',
        '-c:a', 'copy', '-movflags', '+faststart', str(destination)
    ]
    subprocess.run(cmd, check=True)
    return destination

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--genre', default='ai_productivity', choices=GENRE_STRENGTH.keys())
    args = parser.parse_args()
    render(args.source, args.destination, args.genre)
