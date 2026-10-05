import json
from pathlib import Path

def test_cycle250_scene_schema():
    p=Path("quality/cycle250/scene_schema.json")
    d=json.loads(p.read_text(encoding="utf-8"))
    assert d["format"]["width"] == 1080
    assert d["format"]["height"] == 1920
    assert d["format"]["target_seconds"] == 15
    assert len(d["scene_roles"]) == 8
    assert d["publication_gate"] == "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
