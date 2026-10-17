"""Reusable 10-genre motion and publication safety checks (cycle646)."""
from dataclasses import dataclass

GENRES=(
    'AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
    '営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学',
    '旅行・グルメ','商品比較・暮らし'
)

@dataclass(frozen=True)
class RenderPolicy:
    width:int=1080
    height:int=1920
    fps:int=30
    publication:str='NOT_APPROVED'
    human_review:bool=True
    auto_post:bool=False

def motion_filter(fps=30,max_zoom=1.036,zoom_per_frame=0.000075):
    if fps<=0 or not (1<=max_zoom<=1.08) or zoom_per_frame<0:
        raise ValueError('invalid safe motion settings')
    z=f'min(1+on*{zoom_per_frame}, {max_zoom})'
    return f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={fps},format=yuv420p"

def assert_publish_blocked(policy:RenderPolicy):
    assert policy.publication=='NOT_APPROVED'
    assert policy.human_review is True
    assert policy.auto_post is False

def validate_scene_boundaries(bounds,expected_frames=468):
    if len(bounds)!=9 or bounds[0]!=0 or bounds[-1]!=expected_frames:
        raise ValueError('8 scenes / exact frame count required')
    if any(b<=a for a,b in zip(bounds,bounds[1:])):
        raise ValueError('scene boundaries must increase')
    return True
