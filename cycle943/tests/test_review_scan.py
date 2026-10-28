import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from review_scan import beat_at,envelope,ROWS,PALETTES,apply_focus

class ReviewScanTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(PALETTES),10)
    def test_three_review_items(self): self.assertEqual(len(ROWS),3)
    def test_before_scene(self): self.assertIsNone(beat_at(11.59))
    def test_after_scene(self): self.assertIsNone(beat_at(14.5))
    def test_first_beat(self): self.assertEqual(beat_at(12.0)[0],0)
    def test_second_beat(self): self.assertEqual(beat_at(13.0)[0],1)
    def test_third_beat(self): self.assertEqual(beat_at(14.0)[0],2)
    def test_envelope_endpoints(self):
        self.assertEqual(envelope(0),0);self.assertEqual(envelope(1),0)
    def test_envelope_middle(self): self.assertAlmostEqual(envelope(.5),1)
    def test_invalid_envelope(self):
        with self.assertRaises(ValueError): envelope(-.1)
    def test_invalid_genre(self):
        import numpy as np
        with self.assertRaises(ValueError): apply_focus(np.zeros((1920,1080,3),dtype='uint8'),12,'unknown')
    def test_preserves_header_subtitles_warning(self):
        import numpy as np
        f=np.random.default_rng(1).integers(0,256,(1920,1080,3),dtype='uint8')
        original=f.copy();apply_focus(f,13,'ai_productivity')
        self.assertTrue(np.array_equal(f[:570],original[:570]))
        self.assertTrue(np.array_equal(f[1190:],original[1190:]))
        self.assertTrue(np.array_equal(f[:,:88],original[:,:88]))
        self.assertTrue(np.array_equal(f[:,803:],original[:,803:]))
    def test_visible_active_scan(self):
        import numpy as np
        f=np.full((1920,1080,3),80,dtype='uint8');orig=f.copy()
        apply_focus(f,12.1,'ai_productivity')
        self.assertGreater(int(np.abs(f.astype('int16')-orig).sum()),100)
    def test_nonactive_rows_untouched(self):
        import numpy as np
        f=np.full((1920,1080,3),80,dtype='uint8');orig=f.copy()
        apply_focus(f,12.1,'ai_productivity')
        self.assertTrue(np.array_equal(f[865:1165],orig[865:1165]))
    def test_no_change_outside_scene(self):
        import numpy as np
        f=np.full((1920,1080,3),80,dtype='uint8');orig=f.copy()
        apply_focus(f,16.0,'ai_productivity')
        self.assertTrue(np.array_equal(f,orig))
if __name__=='__main__':unittest.main()
