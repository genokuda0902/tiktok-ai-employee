import sys, hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import reuse_story as s

def test_policy():
 assert s.POLICY.endswith('PUBLICATION_NOT_APPROVED')
 assert s.SAFE_Y<=1440 and s.START==522 and s.COUNT==65

def test_phases():
 assert [s.phase(i) for i in (0,21,22,43,44,64)]==[0,0,1,1,2,2]
 for i in (-1,65):
  with pytest.raises(ValueError):s.phase(i)

def test_10_genres():
 assert len(s.GENRES)==10
 for g in s.GENRES:
  s.guard(g,'a'*64)
  assert s.frame(0,g).size==(1080,1440)

def test_distinct_shots():
 hashes=[hashlib.sha256(s.frame(i).tobytes()).hexdigest() for i in (10,30,54)]
 assert len(set(hashes))==3

def test_source_fail_closed():
 for bad in ('', 'a'*63, 'G'*64):
  with pytest.raises(ValueError):s.guard('ai_work',bad)
 with pytest.raises(ValueError):s.guard('unknown','a'*64)

def test_no_publication_paths():
 text=Path(s.__file__).read_text()
 assert 'tiktok.upload' not in text.lower() and 'publish_video(' not in text.lower()
 assert 'PUBLICATION_NOT_APPROVED' in text
