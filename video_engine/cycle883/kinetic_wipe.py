"""Review-only, no-network 10-genre kinetic scene wipes; never uploads private media."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ('ai_productivity', 'beauty', 'romance_psychology', 'money_saving',
          'sales_business', 'career', 'health_lifestyle', 'trivia_science',
          'travel_food', 'product_lifestyle')
FPS, FRAMES, WIDTH, HEIGHT = 30, 691, 1080, 1920
CAPTION_TOP = 1438
CUTS = (89, 170, 251, 336, 422, 510, 588)
HALF_WINDOW = 4
POLICY = {'review_only': True, 'publication_approved': False,
          'external_upload': False, 'automatic_posting': False,
          'source_rights_reviewed': False}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def validate(genre, cuts=CUTS, frames=FRAMES, half=HALF_WINDOW,
             canvas=(WIDTH, HEIGHT), caption_top=CAPTION_TOP):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    w, h = canvas
    if w <= 0 or h <= 0 or not (0 < caption_top <= h - 30):
        raise ValueError('invalid canvas / subtitle safe zone')
    if not cuts or sorted(set(cuts)) != list(cuts):
        raise ValueError('cuts must be ordered and unique')
    if not isinstance(half, int) or not 3 <= half <= 9:
        raise ValueError('wipe too short/long')
    if any(c - half < 1 or c + half >= frames - 1 for c in cuts):
        raise ValueError('wipe outside timeline')
    if any(b - a <= 2 * half + 1 for a, b in zip(cuts, cuts[1:])):
        raise ValueError('overlapping wipes')
    return True

def validate_manifest(manifest, source):
    if any(manifest.get(k) is not v for k, v in POLICY.items()):
        raise ValueError('review-only policy missing / unsafe')
    if manifest.get('source_sha256') != sha256(source):
        raise ValueError('source SHA mismatch')
    if manifest.get('synthetic_ui') is not True:
        raise ValueError('unverified source provenance')
    return True

def make_mask(path, width=WIDTH, caption_top=CAPTION_TOP):
    from PIL import Image, ImageDraw
    mask_w = round(width * 2.45)
    im = Image.new('RGBA', (mask_w, caption_top), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (mask_w - round(width * .24), 0),
               (mask_w, caption_top), (round(width * .24), caption_top)],
              fill=(7, 21, 44, 248))
    for j, alpha in enumerate((32, 65, 110, 170, 220)):
        x = mask_w // 2 - round(width * .10) + j * round(width * .038)
        d.polygon([(x, 0), (x + round(width * .012), 0),
                   (x + round(width * .26), caption_top),
                   (x + round(width * .248), caption_top)],
                  fill=(37, 221, 242, alpha))
    im.save(path)
    return mask_w

def filtergraph(cuts=CUTS, frames=FRAMES, half=HALF_WINDOW,
                width=WIDTH, caption_top=CAPTION_TOP):
    mask_w = round(width * 2.45)
    names = ''.join(f'[w{i}]' for i in range(len(cuts)))
    filters = [f'[1:v]format=rgba,split={len(cuts)}{names}',
               '[0:v]format=yuv420p[v0]']
    for i, cut in enumerate(cuts):
        start, end = cut - half, cut + half
        speed = (mask_w + width) / (2 * half)
        x = f'if(between(n,{start},{end}),-{mask_w}+(n-{start})*{speed:.6f},NAN)'
        filters.append(f"[v{i}][w{i}]overlay=x='{x}':y=0:eval=frame:format=auto[v{i+1}]")
    return ';'.join(filters), f'[v{len(cuts)}]'

def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,sample_rate',
        '-of', 'json', str(path)]))

def render(source, output, manifest_path, report_path, genre='ai_productivity'):
    validate(genre)
    source, output = Path(source), Path(output)
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    validate_manifest(manifest, source)
    p = probe(source)
    video = next(s for s in p['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in p['streams'] if s['codec_type'] == 'audio')
    if (video['width'], video['height'], video['r_frame_rate'],
        int(video.get('nb_frames') or 0), audio['codec_name']) != (WIDTH, HEIGHT, '30/1', FRAMES, 'aac'):
        raise ValueError('incompatible inherited video/audio')
    output.parent.mkdir(parents=True, exist_ok=True)
    mask = output.parent / 'cycle883_private_transition_mask.png'
    make_mask(mask)
    graph, outpad = filtergraph()
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
           '-loop', '1', '-framerate', '30', '-i', str(mask),
           '-filter_complex', graph, '-map', outpad, '-map', '0:a:0',
           '-frames:v', str(FRAMES), '-c:v', 'libx264', '-preset', 'veryfast',
           '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
           '-movflags', '+faststart', str(output)]
    subprocess.run(cmd, check=True, timeout=300)
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output),
                    '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'],
                   check=True, timeout=120)
    q = probe(output)
    result = {'source_sha256': sha256(source), 'output_sha256': sha256(output),
              'genre': genre, 'cuts': list(CUTS), 'wipe_half_frames': HALF_WINDOW,
              'frames': FRAMES, 'duration': q['format']['duration'],
              'streams': q['streams'], 'full_av_decode': 'PASS',
              'speech_semantics': 'UNVERIFIED', 'rights': 'UNVERIFIED',
              'smartphone_playback': 'UNVERIFIED',
              'quality_gate': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    Path(report_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    for name in ('source', 'output', 'manifest', 'report'):
        a.add_argument('--' + name, required=True)
    a.add_argument('--genre', default='ai_productivity')
    x = a.parse_args()
    print(json.dumps(render(x.source, x.output, x.manifest, x.report, x.genre), ensure_ascii=False, indent=2))
