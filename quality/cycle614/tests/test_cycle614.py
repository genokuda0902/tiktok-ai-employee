import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_cycle614 import pulse_frame,palette,PULSE_FRAMES,SIZE,X,Y,GENRES
import json

def test_ten_genres():
 cfg=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
 assert len(cfg)==10
 for k in cfg:
  assert len(palette(k))==3
  assert pulse_frame(12,k).size==(SIZE,SIZE)

def test_rgba_and_transparency():
 for i in (0,5,12,25,39,47):
  im=pulse_frame(i)
  assert im.mode=='RGBA'
  assert im.getpixel((0,0))[3]==0
  assert im.getbbox() is not None or i==0

def test_motion_changes():
 assert pulse_frame(10).tobytes()!=pulse_frame(25).tobytes()

def test_safe_placement():
 assert 0<=X and X+SIZE<900 and Y>350 and Y+SIZE<850

def test_input_validation():
 with pytest.raises(ValueError):pulse_frame(-1)
 with pytest.raises(ValueError):pulse_frame(PULSE_FRAMES)
 with pytest.raises(ValueError):palette('not-a-genre')

def test_fade_and_peak():
 a=pulse_frame(0).getchannel('A').getextrema()[1]
 b=pulse_frame(20).getchannel('A').getextrema()[1]
 c=pulse_frame(47).getchannel('A').getextrema()[1]
 assert a<b and c<b
