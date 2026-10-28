import sys, hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import closing_cta as s

def test_policy_geometry():
 assert s.POLICY.endswith('PUBLICATION_NOT_APPROVED')
 assert s.START==609 and s.COUNT==82 and s.TOTAL==691 and s.SAFE_Y<=1400

def test_timing():
 assert [s.phase(i) for i in (0,26,27,53,54,81)]==[0,0,1,1,2,2]
 for i in (-1,82):
  with pytest.raises(ValueError):s.phase(i)

def test_ten_distinct_genres():
 assert len(s.GENRES)==10
 assert len({v[1] for v in s.GENRES.values()})==10
 for genre in s.GENRES:
  s.guard(genre,'a'*64)
  assert s.frame(60,genre).size==(1080,1400)

def test_three_visual_phases():
 hashes=[hashlib.sha256(s.frame(i).tobytes()).hexdigest() for i in (10,38,70)]
 assert len(set(hashes))==3
 assert s.frame(70).tobytes()!=s.frame(71).tobytes()

def test_source_fail_closed():
 for bad in ('','a'*63,'G'*64):
  with pytest.raises(ValueError):s.guard('ai_work',bad)
 with pytest.raises(ValueError):s.guard('unknown','a'*64)

def test_release_gate_no_posting():
 t=Path(s.__file__).read_text()
 assert 'tiktok.upload' not in t.lower() and 'publish_video(' not in t.lower()
 assert 'PUBLICATION_NOT_APPROVED' in t
 assert '未承認' in t and '手動投稿' in t
