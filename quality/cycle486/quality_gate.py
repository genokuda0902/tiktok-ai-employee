"""Genre-neutral review quality gate for all 10 TikTok genres."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Scene:
    genre: str
    start: float
    end: float
    caption: str
    asset_rights: str = 'SYNTHETIC_LOCAL'

def validate_scenes(scenes, duration, allowed_genres=None):
    if not scenes or not isfinite(duration) or duration <= 0:
        raise ValueError('missing scenes or duration')
    previous = 0.0
    for scene in scenes:
        if allowed_genres is not None and scene.genre not in allowed_genres:
            raise ValueError('unknown genre')
        if scene.asset_rights not in ('SYNTHETIC_LOCAL', 'APPROVED_PUBLIC'):
            raise ValueError('asset rights not verified')
        if not scene.caption or len(scene.caption) > 100:
            raise ValueError('caption invalid')
        if not all(isfinite(x) for x in (scene.start, scene.end)):
            raise ValueError('nonfinite timing')
        if not 0 <= previous <= scene.start < scene.end <= duration + 0.04:
            raise ValueError('scene timing overlap/outside duration')
        previous = scene.end
    return {'scene_count': len(scenes), 'rights': 'CHECKED', 'publication': 'NOT_APPROVED'}

def publication_gate(*, audio_codec, japanese_voice_verified,
                     captions_transcript_verified, semantic_sync_verified,
                     human_approved, rights_approved, auto_post=False):
    if auto_post:
        raise ValueError('automatic posting prohibited')
    checks = {'aac_audio': audio_codec == 'aac',
              'japanese_voice_verified': japanese_voice_verified is True,
              'captions_transcript_verified': captions_transcript_verified is True,
              'semantic_sync_verified': semantic_sync_verified is True,
              'human_approved': human_approved is True,
              'rights_approved': rights_approved is True}
    return {'checks': checks,
            'publication': 'APPROVED_FOR_MANUAL_POST' if all(checks.values()) else 'NOT_APPROVED',
            'auto_post': False}
