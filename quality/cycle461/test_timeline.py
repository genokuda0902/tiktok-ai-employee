from voice_ci import BEATS, validate, synthesize
from unittest.mock import patch
from pathlib import Path
import pytest

def test_timeline():
    assert validate() and len(BEATS)==8
    assert BEATS[0][0]==0 and BEATS[0][1]<=1.5
    assert BEATS[-1][1]==20

def test_all_voice_and_captions():
    assert all(spoken.strip() and caption.strip() for _,_,spoken,caption in BEATS)

def test_no_blank_voice():
    bad=list(BEATS)
    s,e,_,c=bad[1]
    bad[1]=(s,e,"",c)
    with pytest.raises(ValueError):
        validate(bad)

def test_no_overlap():
    bad=list(BEATS)
    s,e,v,c=bad[2]
    bad[2]=(s+.1,e,v,c)
    with pytest.raises(ValueError):
        validate(bad)

def test_missing_engine_fails_closed(tmp_path):
    with patch("voice_ci.shutil.which",return_value=None):
        with pytest.raises(RuntimeError,match="Missing free Japanese TTS"):
            synthesize(tmp_path)
