"""Cycle744 internal QA: deterministic synthetic scene contract."""
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "cinematic_workbook.py"
spec = importlib.util.spec_from_file_location("workbook", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_scene_dimensions():
    assert (mod.W, mod.H, mod.FPS, mod.FRAMES) == (1080, 1920, 30, 99)

def test_sample_sum():
    assert mod.validate_data() == 65

def test_ten_genres():
    assert len(mod.PALETTES) == 10

def test_no_publication_without_approval():
    assert mod.validate_provenance({
        "source_kind": "synthetic_demo",
        "release": "NOT_APPROVED",
        "auto_post": False
    })

def test_safe_regions():
    assert mod.verify_safe_regions()
