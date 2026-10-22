import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_stages():
    cfg=json.loads((ROOT/'config/hook.json').read_text())
    assert cfg['resolution']==[1080,1920]
    assert cfg['stages'][1]['start']==0.167
    assert cfg['stages'][2]['start']==1
def test_review():
    cfg=json.loads((ROOT/'config/hook.json').read_text())
    assert cfg['publication_approved'] is False
    assert cfg['review']=='HUMAN_REVIEW'
