import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_cycle621 import wipe_frame, START, END

def test_window():
    assert (START, END) == (244, 257)

def test_wipe_no_blend():
    a = np.full((64, 64, 3), 12, dtype=np.uint8)
    b = np.full((64, 64, 3), 220, dtype=np.uint8)
    for i in range(START, END + 1):
        out = wipe_frame(a, b, i)
        assert set(np.unique(out[:, :, 0])).issubset({12, 220, 218})
