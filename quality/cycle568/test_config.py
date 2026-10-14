import json
from pathlib import Path

def test_cycle568_config():
    config = json.loads((Path(__file__).parent / "config.json").read_text())
    assert config["cycle"] == 568
    assert config["scene"] == 4
    assert config["start_frame"] == 215
    assert config["frame_count"] == 29
    assert config["resolution"] == [1080, 1920]
    assert config["review"] == "HUMAN_REVIEW"
    assert config["publication"] == "NOT_APPROVED"
