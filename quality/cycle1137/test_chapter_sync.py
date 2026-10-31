import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from chapter_sync import PALETTES, make_sweep, sweep_active, sweep_x_expr

CUTS=[3.133333,5.6,8.233333,11.,13.733333,16.633333,19.166667]
OLD=[2.8,5.6,8.4,11.2,14.,16.8,19.6]

class ChapterSyncTests(unittest.TestCase):
    def test_ten_distinct_genres(self):
        self.assertEqual(len(PALETTES),10)
        self.assertEqual(len(set(PALETTES.values())),10)
    def test_original_asset_generation(self):
        with TemporaryDirectory() as d:
            for genre,color in PALETTES.items():
                im=make_sweep(Path(d)/(genre+'.png'),color,120,16)
                self.assertEqual(im.size,(120,16))
                self.assertGreater(im.getpixel((60,8))[3],30)
                self.assertEqual(im.getpixel((0,0))[3],0)
    def test_real_cut_corrects_previous_early_flash(self):
        self.assertFalse(sweep_active(2.9,CUTS))
        self.assertTrue(sweep_active(2.9,OLD))
        self.assertTrue(sweep_active(3.2,CUTS))
        self.assertFalse(sweep_active(3.2,OLD))
    def test_all_real_cuts_active(self):
        self.assertTrue(all(sweep_active(c+.07,CUTS) for c in CUTS))
    def test_no_fixed_modulo(self):
        expr=sweep_x_expr(CUTS)
        self.assertIn('3.133333',expr)
        self.assertIn('19.166667',expr)
        self.assertNotIn('mod(',expr)
        self.assertIn('NAN',expr)
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError): sweep_x_expr([1,1.1])
    def test_nonpositive_duration_rejected(self):
        with self.assertRaises(ValueError): sweep_x_expr([1],duration=0)

if __name__=='__main__': unittest.main()
