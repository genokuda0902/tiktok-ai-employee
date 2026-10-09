import json
from pathlib import Path

def test_storyboard_duration():
    data = json.loads((Path(__file__).parent / "storyboard.json").read_text(encoding="utf-8"))
    assert abs(sum(scene["seconds"] for scene in data["scenes"]) - 20) < 0.01
    assert len(data["scenes"]) == 8
    assert data["approval"] == "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
