"""Review-only early evidence preview, sourced from the same private demo MP4.

Not original v33. No media or screenshots are stored in the public repository.
The 10 genre profiles have separate evidence rules; only ai_work geometry is reviewed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EXPECTED_SOURCE_SHA = 'ac5fcfcfc744edbf9ec4cf7080e53ce88a9e7a9512021593119188ed66bbb22a'
WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
CAPTION_TOP = 1490
CARD_X, CARD_Y, CARD_W, CARD_H = 490, 620, 410, 310
PROOF_TIME = 13.8
GENRE_EVIDENCE = {
    'ai_work': 'verified fictional spreadsheet total',
    'finance': 'source-dated calculations, no investment promises',
    'history': 'source-dated primary evidence',
    'science': 'experiment or peer-reviewed source',
    'health': 'reviewed medical sources, no personal health data',
    'travel': 'verified destination and current dates',
    'food': 'original cooking result and ingredient proof',
    'career': 'original workflow demonstration',
    'education': 'worked example and checked answer',
    'lifestyle': 'original before/after with provenance',
}
REVIEWED_GENRES = frozenset({'ai_work'})


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate(source: str | Path, genre: str, publication_approved: bool = False,
             review_only: bool = True) -> None:
    if genre not in GENRE_EVIDENCE:
        raise ValueError('unknown genre')
    if genre not in REVIEWED_GENRES:
        raise ValueError('evidence geometry/rights have not been reviewed for this genre')
    if publication_approved is not False or review_only is not True:
        raise ValueError('manual employee review is mandatory; publication unapproved')
    if not Path(source).is_file() or sha256(source) != EXPECTED_SOURCE_SHA:
        raise ValueError('source SHA mismatch or unavailable private source')
    if CARD_X < 0 or CARD_Y < 0 or CARD_X + CARD_W > WIDTH or CARD_Y + CARD_H >= CAPTION_TOP:
        raise ValueError('proof card would overlap the protected caption area')


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    base = 'NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
    path = Path('/usr/share/fonts/opentype/noto') / base
    if not path.exists():
        raise FileNotFoundError(f'Japanese font unavailable: {path}')
    return ImageFont.truetype(str(path), size)


def make_card(proof_frame: Image.Image) -> Image.Image:
    """Create an honest mini-proof, with a crop from the existing fictional Calc demo."""
    if proof_frame.size != (WIDTH, HEIGHT):
        raise ValueError('proof source must be a 1080x1920 frame')
    card = Image.new('RGBA', (CARD_W, CARD_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((1, 1, CARD_W-2, CARD_H-2), radius=23,
                        fill=(3, 31, 43, 250), outline=(77, 234, 204, 255), width=4)
    d.text((21, 16), '検算の結果を先に表示', font=font(25, True), fill=(238, 255, 251, 255))
    d.rounded_rectangle((18, 61, CARD_W-19, 204), radius=8,
                        fill=(255, 255, 255, 255))
    # The original source at 13.8s has final 46/29 totals in a real Calc recording.
    # Crop the two bottom rows; no fabricated GUI, no external image or private data.
    crop = proof_frame.crop((90, 750, 700, 940)).convert('RGB')
    crop = crop.resize((CARD_W-44, 130), Image.Resampling.LANCZOS)
    card.paste(crop, (22, 67))
    d.text((23, 212), 'A：12＋16＋18＝46', font=font(23, True), fill=(140, 251, 226, 255))
    d.text((23, 247), 'B：8＋9＋12＝29', font=font(23, True), fill=(225, 245, 252, 255))
    d.text((290, 287), '架空データ', font=font(14), fill=(170, 203, 208, 255))
    return card


def extract_frame(source: str | Path, seconds: float, dest: str | Path) -> None:
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(seconds),
           '-i', str(source), '-frames:v', '1', str(dest)]
    subprocess.run(cmd, check=True)


def render(source: str | Path, output: str | Path, genre: str = 'ai_work') -> dict:
    validate(source, genre)
    source, output = Path(source), Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle960_') as tmp:
        frame_path = Path(tmp) / 'proof.png'
        card_path = Path(tmp) / 'card.png'
        extract_frame(source, PROOF_TIME, frame_path)
        with Image.open(frame_path) as proof:
            make_card(proof.convert('RGB')).save(card_path)
        # Alpha fades prevent a hard jump; overlay remains strictly above captions.
        filters = (
            '[1:v]format=rgba,'
            'fade=t=in:st=0.35:d=0.18:alpha=1,'
            'fade=t=out:st=2.06:d=0.28:alpha=1[proof];'
            f'[0:v][proof]overlay=x={CARD_X}:y={CARD_Y}:'
            "enable='between(t,0.35,2.34)':format=auto[v]"
        )
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-i', str(source), '-loop', '1', '-framerate', str(FPS), '-i', str(card_path),
               '-filter_complex', filters, '-map', '[v]', '-map', '0:a:0',
               '-frames:v', str(FRAMES), '-c:v', 'libx264', '-preset', 'veryfast',
               '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
               '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True, timeout=210)
    return {'source_sha256': sha256(source), 'output_sha256': sha256(output),
            'source_proof_time': PROOF_TIME, 'evidence': GENRE_EVIDENCE[genre],
            'card': [CARD_X, CARD_Y, CARD_W, CARD_H], 'caption_top': CAPTION_TOP,
            'active_seconds': [0.35, 2.34], 'reviewed_genre': genre,
            'publication_status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--qa', required=True)
    p.add_argument('--genre', default='ai_work')
    a = p.parse_args()
    data = render(a.source, a.output, a.genre)
    Path(a.qa).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False))
