from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_cycle619 import check_patches, replacement_frame

def test_patch_count():
    assert check_patches() == 17

def test_boundary_mapping():
    assert replacement_frame(219) == 215
    assert replacement_frame(220) == 223
    assert replacement_frame(286) == 279
    assert replacement_frame(287) == 290
