from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/"render.py"
spec=importlib.util.spec_from_file_location("cycle1288",P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def test_scene_contract():
    assert len(mod.SCENES)==4
    assert all(head and sub for head,sub in mod.SCENES)
def test_review_only():
    assert "REVIEW_ONLY" in P.read_text()
    assert '"-an"' in P.read_text()
