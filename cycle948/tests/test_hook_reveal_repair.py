import hashlib
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'src'))
from hook_reveal_repair import HookSpec, GENRES, sha256, alpha_feather, make_patch
H='0'*64

@pytest.mark.parametrize('genre',GENRES)
def test_ten_genre_common_engine(genre):
    HookSpec(genre,(565,596,445,476),2.45,2.18,0.2,H).validate()

def test_rejects_caption_overlap():
    with pytest.raises(ValueError): HookSpec('ai_work',(500,1400,400,300),2.45,2.18,0.2,H).validate()

def test_rejects_wrong_order():
    with pytest.raises(ValueError): HookSpec('ai_work',(500,600,400,300),1.0,2.0,0.2,H).validate()

def test_rejects_unpinned_source():
    with pytest.raises(ValueError): HookSpec('ai_work',(500,600,400,300),2.45,2.18,0.2,'').validate()

def test_rejects_unknown_genre():
    with pytest.raises(ValueError): HookSpec('fake',(500,600,400,300),2.45,2.18,0.2,H).validate()

def test_sha256(tmp_path):
    p=tmp_path/'source';p.write_bytes(b'abc')
    assert sha256(p)==hashlib.sha256(b'abc').hexdigest()


def test_feather_alpha():
    m=alpha_feather(80,60)
    assert m.shape==(60,80) and m[0,0]==0 and m[30,40]==255
    assert 0<m[6,40]<255

def test_rejects_source_hash_mismatch(tmp_path):
    p=tmp_path/'fake.mp4';p.write_bytes(b'not an MP4')
    spec=HookSpec('ai_work',(500,600,400,300),2.45,2.18,0.2,H)
    with pytest.raises(RuntimeError,match='hash mismatch'):
        make_patch(p,spec,tmp_path/'patch.png')
