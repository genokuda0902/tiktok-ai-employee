"""Experimental genre configuration; no posting or production wiring."""
import json
from pathlib import Path

PROFILE_PATH = Path(__file__).resolve().parents[1] / 'config' / 'genre_profiles.v1.json'
REQUIRED = {'label', 'hook', 'visual', 'beats', 'primary_metric', 'qa'}
ALLOWED_METRICS = {'follows_per_1000_views', 'saves_per_1000_views', 'shares_per_1000_views', 'completion_rate'}


def load_profiles(path=PROFILE_PATH):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config.get('schema_version') != 1 or config.get('status') != 'experimental_not_connected_to_production':
        raise ValueError('Unsupported genre profile schema or status')
    policy = config.get('default_policy', {})
    if policy.get('publish_mode') != 'employee_manual_only' or policy.get('quality_approval_required') is not True or policy.get('missing_metrics') != 'null_not_zero' or policy.get('private_data') != 'block':
        raise ValueError('Required safety policy missing')
    genres = config.get('genres')
    if not isinstance(genres, dict) or len(genres) != 10:
        raise ValueError('Expected ten distinct genre profiles')
    for genre_id, profile in genres.items():
        if not isinstance(profile, dict) or not REQUIRED.issubset(profile):
            raise ValueError(f'Invalid profile: {genre_id}')
        if profile['primary_metric'] not in ALLOWED_METRICS:
            raise ValueError(f'Invalid metric: {genre_id}')
        for key in ('visual', 'beats', 'qa'):
            if not isinstance(profile[key], list) or not profile[key] or not all(isinstance(item, str) and item for item in profile[key]):
                raise ValueError(f'Invalid {key}: {genre_id}')
    return config


def plan_for_genre(genre_id, path=PROFILE_PATH):
    """Return a profile, not a publishable or approved video plan."""
    profiles = load_profiles(path)['genres']
    if genre_id not in profiles:
        raise ValueError('Unknown genre; generation blocked')
    return dict(profiles[genre_id])


def metric_value(metrics, metric_name):
    """Unknown/missing metrics stay None; never impute zero."""
    if metric_name not in ALLOWED_METRICS:
        raise ValueError('Unknown metric')
    if not isinstance(metrics, dict):
        return None
    value = metrics.get(metric_name)
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0 else None
