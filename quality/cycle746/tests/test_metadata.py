import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_genres():
    assert len(json.loads((ROOT/"config/genres.json").read_text())["genres"])==10

def test_two_voice_cues():
    srt=(ROOT/"config/phrase_cues.srt").read_text()
    assert "画面につなげば" in srt
    assert "操作できる" in srt

def test_human_review_required():
    readme=(ROOT/"README.md").read_text()
    assert "employee approval" in readme.lower()
    assert "No automatic posting" in readme
