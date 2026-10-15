import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build_cycle602 import create_ambient,accent_for,GENRES,START_Y,ART_H,ART_W,sha256

class TestAmbient(unittest.TestCase):
    def test_ten_genres(self):
        names=json.loads(GENRES.read_text(encoding='utf8'))['genres']
        self.assertEqual(len(names),10)
        for name in names:self.assertEqual(len(accent_for(name)),3)
    def test_invalid_genre_rejected(self):
        with self.assertRaises(ValueError):accent_for('not-a-genre')
    def test_size(self):self.assertEqual(create_ambient().size,(ART_W,ART_H))
    def test_top_fade(self):self.assertEqual(create_ambient().getpixel((200,0))[3],0)
    def test_full_opacity_below_fade(self):self.assertEqual(create_ambient().getpixel((200,300))[3],255)
    def test_nonblank_art(self):
        art=create_ambient();self.assertNotEqual(art.getpixel((350,400)),art.getpixel((800,400)))
    def test_no_caption_overlap(self):self.assertGreaterEqual(START_Y,1250)
    def test_determinism(self):self.assertEqual(create_ambient().tobytes(),create_ambient().tobytes())

if __name__=='__main__':unittest.main()
