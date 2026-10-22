from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from data_story_card import card, GENRES, STAGES

def test_ten_genres():
    assert len(GENRES)==10
    for g in GENRES: assert card(0,g).size==(1080,1920)

def test_frame_windows():
    assert STAGES==((96,128),(129,161),(162,194))

def test_distinct():
    assert len({card(i).tobytes() for i in range(3)})==3
