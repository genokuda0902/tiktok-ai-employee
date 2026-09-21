"""Review-only adapter: genre scene manifest -> existing FFmpeg video stack.

Requires locally supplied, approved still images and narrated audio per scene.
Does not create assets, approve quality, deliver, or publish anything.
"""
import json
import subprocess
import tempfile
from pathlib import Path

from genre_profiles import plan_for_genre


def _motion_filter(scene_index):
    """Deterministic per-scene motion to avoid a repetitive static-slideshow feel."""
    base = "scale=1200:2134:force_original_aspect_ratio=increase,crop=1200:2134"
    motions = (
        "zoompan=z='min(zoom+0.0010,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
        "zoompan=z='min(zoom+0.0008,1.08)':x='max(0,(iw-iw/zoom)*on/(30*4))':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
        "zoompan=z='min(zoom+0.0008,1.08)':x='max(0,iw-iw/zoom-(iw-iw/zoom)*on/(30*4))':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
        "zoompan=z='min(zoom+0.0007,1.07)':x='iw/2-(iw/zoom/2)':y='max(0,(ih-ih/zoom)*on/(30*4))':d=1:s=1080x1920:fps=30",
        "zoompan=z='min(zoom+0.0012,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30",
    )
    return base + ',' + motions[scene_index % len(motions)]


def _caption_filter(scene_index, caption_path):
    """High-contrast mobile-safe captions; scene zero gets a stronger 0-2s hook treatment."""
    if scene_index == 0:
        return (
            "drawbox=x=54:y=180:w=972:h=330:color=black@0.82:t=fill,"
            f"drawtext=textfile={caption_path}:fontcolor=white:fontsize=72:borderw=4:bordercolor=black:"
            "x=(w-text_w)/2:y=275:enable='between(t,0,2.2)',"
            "drawbox=x=54:y=1450:w=972:h=280:color=black@0.78:t=fill,"
            f"drawtext=textfile={caption_path}:fontcolor=white:fontsize=52:borderw=3:bordercolor=black:"
            "x=(w-text_w)/2:y=1510:enable='gte(t,2.2)'"
        )
    return (
        "drawbox=x=54:y=1450:w=972:h=280:color=black@0.78:t=fill,"
        f"drawtext=textfile={caption_path}:fontcolor=white:fontsize=52:borderw=3:bordercolor=black:"
        "x=(w-text_w)/2:y=1510"
    )


def render_review_video(manifest_path, asset_root, output_path, ffmpeg='ffmpeg'):
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1 or manifest.get('status') != 'draft_review_only' or manifest.get('render_ready') is not False or manifest.get('quality_approved') is not False or manifest.get('publish_mode') != 'employee_manual_only':
        raise ValueError('Only unapproved, manual-posting draft manifests may be rendered')
    profile = plan_for_genre(manifest.get('genre_id'))
    scenes = manifest.get('scenes')
    if not isinstance(scenes, list) or len(scenes) != len(profile['beats']):
        raise ValueError('Scene count does not match genre')
    root = Path(asset_root).resolve(strict=True)
    out = Path(output_path).resolve()
    if out.suffix.lower() != '.mp4' or out.exists():
        raise ValueError('Output must be a new MP4 file')
    prepared = []
    for i, (scene, beat) in enumerate(zip(scenes, profile['beats'])):
        if not isinstance(scene, dict) or scene.get('index') != i or scene.get('beat') != beat or scene.get('visual_kind') not in profile['visual']:
            raise ValueError('Scene does not match genre plan')
        if not isinstance(scene.get('asset_id'), str) or not scene['asset_id'].strip():
            raise ValueError('Approved asset reference required')
        if scene.get('asset_approved') is not True or scene.get('audio_approved') is not True:
            raise ValueError('Explicit image and audio approvals required')
        if not isinstance(scene.get('narration'), str) or not scene['narration'].strip() or not isinstance(scene.get('caption'), str) or not scene['caption'].strip():
            raise ValueError('Narration and caption required')
        seconds = scene.get('duration_seconds')
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not 1 <= seconds <= 20:
            raise ValueError('Scene duration must be 1-20 seconds')
        files = []
        for key, suffixes in [('image_path', {'.png', '.jpg', '.jpeg'}), ('audio_path', {'.wav', '.mp3', '.m4a'})]:
            relative = scene.get(key)
            if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
                raise ValueError('Local relative asset path required')
            file = (root / relative).resolve(strict=True)
            if not file.is_relative_to(root) or not file.is_file() or file.suffix.lower() not in suffixes:
                raise ValueError('Asset outside approved root or unsupported format')
            files.append(file)
        prepared.append((scene, files[0], files[1], seconds))
    if not 15 <= sum(item[3] for item in prepared) <= 120:
        raise ValueError('Total video duration outside review limits')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        tmp = Path(temp)
        clips = []
        for i, (scene, image, audio, seconds) in enumerate(prepared):
            caption = tmp / f'caption_{i}.txt'
            caption.write_text(scene['caption'], encoding='utf-8')
            clip = tmp / f'scene_{i}.mp4'
            motion = _motion_filter(i)
            vf = motion + ',' + _caption_filter(i, caption)
            subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-loop', '1', '-framerate', '30', '-i', str(image), '-i', str(audio), '-t', str(seconds), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-af', 'apad', '-movflags', '+faststart', str(clip)], check=True)
            clips.append(clip)
        listing = tmp / 'clips.txt'
        listing.write_text(''.join("file '" + str(clip) + "'\n" for clip in clips), encoding='utf-8')
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', '-movflags', '+faststart', str(out)], check=True)
    return {'output': str(out), 'status': 'rendered_unverified_review_only', 'quality_approved': False, 'publish_mode': 'employee_manual_only'}
