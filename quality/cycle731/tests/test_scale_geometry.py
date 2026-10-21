import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from scale_geometry import widths

class TestScaleGeometry(unittest.TestCase):
    def test_initial(self):self.assertEqual(widths(0),(0,0))
    def test_final(self):self.assertEqual(widths(1),(236,238))
    def test_late_reveal(self):self.assertEqual(widths(.25)[1],0)
    def test_progress(self):self.assertLess(widths(.3)[0],widths(.7)[0])
