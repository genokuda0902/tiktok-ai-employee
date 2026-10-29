"""cycle951: review-only arithmetic-evidence cue and fail-closed caption semantics gate.

The cue describes fictional values already visible in the local source video.
No ASR, licensing, publication approval, automatic posting or external upload is provided.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

GENRES = ('ai_work', 'finance', 'business', 'education', 'lifestyle',
          'health', 'travel', 'food', 'technology', 'career')
W, H, FPS, FRAMES = 1080, 1920, 30, 691
BAND_PHASE1 = (76, 1085, 370, 70)
BAND_PHASE2 = (76, 1140, 370, 75)
CAPTION_TOP = 1490
PHASE1 = (11.75, 13.45)
PHASE2 = (13.45, 14.35)
SOURCE_SHA = 'a28f54e76e4fd54395d2003c0b403a63a5fdc3af9d86a3c4740811abdf66ab07'


@dataclass(frozen=True)
class Evidence:
    genre: str
    fictional: bool
    approved_for_publication: bool
    row_a: tuple[int, ...]
    row_b: tuple[int, ...]
    total_a: int
    total_b: int
    label: str

    def validate(self) -> None:
        if self.genre not in GENRES:
            raise ValueError('unsupported genre')
        if self.approved_for_publication:
            raise ValueError('review-only renderer cannot publish')
        if not self.fictional:
            raise ValueError('only fictional approved-in-source demo numbers allowed')
        if not self.label or len(self.label) > 40:
            raise ValueError('missing or too long evidence label')
        if not (2 <= len(self.row_a) <= 12 and len(self.row_a) == len(self.row_b)):
            raise ValueError('invalid evidence rows')
        for n in (*self.row_a, *self.row_b, self.total_a, self.total_b):
            if not isinstance(n, int) or isinstance(n, bool) or not (0 <= n <= 999_999):
                raise ValueError('invalid evidence number')
        if sum(self.row_a) != self.total_a or sum(self.row_b) != self.total_b:
            raise ValueError('arithmetic inconsistency; do not render')


def make_ai_work_evidence() -> Evidence:
    return Evidence('ai_work', True, False, (12, 16, 18), (8, 9, 12), 46, 29, '架空データ')


def semantic_gate(*, transcript: str | None, caption: str | None,
                  independent_asr: bool, employee_approved: bool) -> dict:
    """Do not mistake existing audio, a VAD result or a copied script for ASR proof.

    Only a supplied *independently obtained* transcript can pass exact-text check;
    publication still requires separate asset and employee approvals.
    """
    if not independent_asr or not transcript or not caption:
        return {'semantic_status': 'UNVERIFIED', 'caption_match': None,
                'employee_approved': bool(employee_approved), 'publication_allowed': False}
    import unicodedata
    normalize = lambda s: ''.join(ch for ch in unicodedata.normalize('NFKC', s)
                                  if not ch.isspace() and ch not in '、。,.!！?？')
    matches = normalize(transcript) == normalize(caption)
    return {'semantic_status': 'TEXT_MATCH_ONLY' if matches else 'MISMATCH',
            'caption_match': matches, 'employee_approved': bool(employee_approved),
            'publication_allowed': False}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def probe(path: Path) -> dict:
    cmd = ['ffprobe', '-v', 'error', '-show_entries',
           'stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames,sample_rate,channels:format=duration',
           '-of', 'json', str(path)]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


def validate_source(source: Path, expected_sha: str, evidence: Evidence) -> dict:
    evidence.validate()
    if not source.is_file() or not expected_sha or len(expected_sha) != 64:
        raise ValueError('explicit local source and SHA256 required')
    actual = sha256(source)
    if actual != expected_sha:
        raise ValueError('source SHA256 mismatch; refusing unreviewed input')
    info = probe(source)
    v = next((x for x in info['streams'] if x['codec_type'] == 'video'), None)
    a = next((x for x in info['streams'] if x['codec_type'] == 'audio'), None)
    if not v or (v.get('width'), v.get('height'), v.get('avg_frame_rate'),
                 int(v.get('nb_frames', 0))) != (W, H, '30/1', FRAMES):
        raise ValueError('unexpected video dimensions, fps or frame count')
    if not a or (a.get('codec_name'), a.get('sample_rate'), a.get('channels')) != ('aac', '48000', 2):
        raise ValueError('unexpected audio format')
    if not all(0 <= b[0] and b[0] + b[2] <= W and b[1] + b[3] < CAPTION_TOP
               for b in (BAND_PHASE1, BAND_PHASE2)):
        raise ValueError('cue would overlap protected subtitle region')
    if not (0 <= PHASE1[0] < PHASE1[1] <= PHASE2[0] < PHASE2[1] <= FRAMES/FPS):
        raise ValueError('invalid chronological cue timings')
    return info


def filtergraph(text_1: Path, text_2: Path, font: Path) -> str:
    """Follow safe blank areas as the original scene micro-motion shifts."""
    stages = []
    for (start, end), label, color, band in [
        (PHASE1, text_1, '0xF8B879', BAND_PHASE1),
        (PHASE2, text_2, '0x6BF5D7', BAND_PHASE2),
    ]:
        x, y, w, h = band
        en = f'between(t,{start:.2f},{end:.2f})'
        stages.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x071D31@0.95:t=fill:enable=\'{en}\'')
        stages.append(f'drawbox=x={x}:y={y}:w=5:h={h}:color={color}:t=fill:enable=\'{en}\'')
        stages.append(f'drawtext=fontfile={font}:textfile={label}:fontcolor=white:fontsize=23:line_spacing=4:x={x+14}:y={y+7}:enable=\'{en}\'')
    return ','.join(stages)


def render(source: Path, output: Path, expected_sha: str, evidence: Evidence,
           font: Path, qa_path: Path) -> dict:
    if source.resolve() == output.resolve():
        raise ValueError('never overwrite the source')
    validate_source(source, expected_sha, evidence)
    if evidence.genre != 'ai_work':
        raise ValueError('other genres require a new approved geometry and source-ledger review')
    if not font.is_file():
        raise ValueError('Japanese font unavailable')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle951_') as tmp:
        first, second = Path(tmp)/'phase1.txt', Path(tmp)/'phase2.txt'
        first.write_text('入力中：合計は未確定\n再計算後に照合する', encoding='utf-8')
        second.write_text('検算 A: 12+16+18=46\n確認 B: 8+9+12=29', encoding='utf-8')
        vf = filtergraph(first, second, font)
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
               '-vf', vf, '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264',
               '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
               '-c:a', 'copy', '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True)
    info = probe(output)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'],
                   check=True, capture_output=True)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v.get('width'), v.get('height'), v.get('avg_frame_rate'), int(v.get('nb_frames', 0))) != (W,H,'30/1',FRAMES):
        raise RuntimeError('output video verification failed')
    if (a.get('codec_name'), a.get('sample_rate')) != ('aac', '48000'):
        raise RuntimeError('output audio verification failed')
    qa = {'cycle': 951, 'source_sha256': expected_sha, 'output_sha256': sha256(output),
          'genre': evidence.genre, 'scene': 'scene05', 'new_change': 'two-stage arithmetic evidence cue',
          'phase1_seconds': PHASE1, 'phase2_seconds': PHASE2,
          'fictional_values': {'a': list(evidence.row_a), 'b': list(evidence.row_b),
                               'total_a': evidence.total_a, 'total_b': evidence.total_b},
          'subtitle_region_y_min': CAPTION_TOP, 'cue_regions': [BAND_PHASE1, BAND_PHASE2],
          'video': {'codec': v['codec_name'], 'width': W, 'height': H, 'fps': FPS,
                    'frames': FRAMES, 'duration': float(info['format']['duration'])},
          'audio': {'codec': a['codec_name'], 'sample_rate': int(a['sample_rate']),
                    'channels': a['channels']},
          'full_av_decode': 'PASS', 'semantic_gate': semantic_gate(transcript=None, caption=None,
                    independent_asr=False, employee_approved=False),
          'status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
          'external_upload': False, 'posting': False}
    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    return qa


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, type=Path)
    p.add_argument('--source-sha256', required=True)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--qa', required=True, type=Path)
    p.add_argument('--font', default='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', type=Path)
    p.add_argument('--genre', default='ai_work', choices=GENRES)
    args = p.parse_args()
    if args.genre != 'ai_work':
        raise SystemExit('genre-specific source/geometry approval is required before rendering')
    report = render(args.source, args.output, args.source_sha256, make_ai_work_evidence(), args.font, args.qa)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
