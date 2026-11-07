from pathlib import Path
import ast

SOURCE = Path(__file__).resolve().parents[1] / "render.py"

def test_four_scenes():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    scenes = next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SCENES" for t in n.targets))
    assert len(ast.literal_eval(scenes)) == 4

def test_explicit_review_only_and_no_audio():
    code = SOURCE.read_text(encoding="utf-8")
    assert "REVIEW ONLY" in code
    assert '"-an"' in code
    assert "1080" not in code  # this is a 720p review sample, not a 1080p claim
