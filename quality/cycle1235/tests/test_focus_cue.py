import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from focus_cue import PALETTES, validate_rect, validate_times, make_cue
from PIL import Image

class FocusCueTest(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(PALETTES), 10)
    def test_palette_distinct(self): self.assertEqual(len(set(PALETTES.values())), 10)
    def test_valid_rect(self): self.assertEqual(validate_rect((510, 970, 180, 80)), (510, 970, 180, 80))
    def test_reject_subtitle(self):
        with self.assertRaises(ValueError): validate_rect((500, 1450, 200, 100))
    def test_reject_edge(self):
        with self.assertRaises(ValueError): validate_rect((1010, 500, 100, 100))
    def test_reject_short(self):
        with self.assertRaises(ValueError): validate_times(0.1, 0.4, 3)
    def test_reject_beyond_duration(self):
        with self.assertRaises(ValueError): validate_times(2.0, 3.5, 3)
    def test_fade_limit(self): self.assertEqual(validate_times(1.0, 2.0, 3.0), .25)
    def test_overlay_transparent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'cue.png'
            make_cue(path, 'ai', (510, 970, 180, 80))
            im = Image.open(path)
            self.assertEqual(im.size, (180, 80))
            self.assertLessEqual(im.getpixel((0, 0))[3], 2)
            self.assertGreater(max(im.getchannel('A').getextrema()), 0)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): make_cue('/tmp/unused.png', 'invalid', (510, 970, 180, 80))

if __name__ == '__main__': unittest.main()
