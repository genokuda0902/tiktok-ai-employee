"""Create review-only scene manifests from genre profiles; never render or publish."""
import json
from pathlib import Path

from genre_profiles import plan_for_genre


def build_scene_manifest(genre_id, topic, assets, evidence=None, profile_path=None):
    """Build a draft only when every beat has an explicitly approved asset.

    assets maps each beat to {'asset_id': str, 'approved': True, 'kind': str}.
    No asset bytes or credentials are read or copied by this module.
    """
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError('Topic required')
    profile = plan_for_genre(genre_id, profile_path) if profile_path else plan_for_genre(genre_id)
    if not isinstance(assets, dict):
        raise ValueError('Approved asset mapping required')
    scenes = []
    for index, beat in enumerate(profile['beats']):
        asset = assets.get(beat)
        if not isinstance(asset, dict) or asset.get('approved') is not True:
            raise ValueError(f'Approved asset missing for beat: {beat}')
        if not isinstance(asset.get('asset_id'), str) or not asset['asset_id'].strip():
            raise ValueError(f'Asset ID missing for beat: {beat}')
        if asset.get('kind') not in profile['visual']:
            raise ValueError(f'Visual type not permitted for beat: {beat}')
        scenes.append({'index': index, 'beat': beat, 'asset_id': asset['asset_id'], 'visual_kind': asset['kind'], 'narration': None, 'caption': None, 'duration_seconds': None})
    if evidence is not None and (not isinstance(evidence, list) or not all(isinstance(e, str) and e.strip() for e in evidence)):
        raise ValueError('Evidence must be a list of nonempty source references')
    return {'schema_version': 1, 'status': 'draft_review_only', 'genre_id': genre_id, 'genre_label': profile['label'], 'topic': topic.strip(), 'hook_strategy': profile['hook'], 'scenes': scenes, 'qa_requirements': profile['qa'], 'primary_metric': profile['primary_metric'], 'evidence': evidence or [], 'quality_approved': False, 'delivery_approved': False, 'publish_mode': 'employee_manual_only', 'render_ready': False}


def save_manifest(manifest, destination):
    if manifest.get('status') != 'draft_review_only' or manifest.get('render_ready') is not False or manifest.get('quality_approved') is not False:
        raise ValueError('Only unapproved draft manifests may be saved')
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return path
