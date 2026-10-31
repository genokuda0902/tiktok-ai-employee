import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from voice_safe_cuts import SOURCE_CUTS,snap_cuts,pts_expression,metadata

class TestPauseCuts(unittest.TestCase):
    def test_snap(self):
        pauses=[(2.965,3.31),(5.448,5.78),(8.069,8.405),(10.835,11.161),(13.576,13.918),(16.395,16.898),(18.970,19.343)]
        self.assertEqual(snap_cuts(SOURCE_CUTS,pauses),[0,94,168,247,330,412,499,575,675])
    def test_fallback(self):
        self.assertEqual(snap_cuts(SOURCE_CUTS,[]),SOURCE_CUTS)
    def test_expression(self):
        e=pts_expression(SOURCE_CUTS,SOURCE_CUTS)
        self.assertIn('lt(N,79)',e)
        self.assertIn('30*TB',e)
    def test_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'meta'
            metadata(p,SOURCE_CUTS)
            self.assertEqual(p.read_text().count('[CHAPTER]'),8)

if __name__=='__main__':unittest.main()
