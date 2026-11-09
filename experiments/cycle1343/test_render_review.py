from pathlib import Path
import importlib.util

path = Path(__file__).with_name("render_review.py")
spec = importlib.util.spec_from_file_location("render_review", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_scenes_are_distinct():
    assert len(mod.SCENES) == 5
    assert len({x[0] for x in mod.SCENES}) == 5

def test_no_private_data_or_publish_instruction():
    script = " ".join(" ".join(scene) for scene in mod.SCENES)
    assert "架空" in script
    assert "投稿" not in script
