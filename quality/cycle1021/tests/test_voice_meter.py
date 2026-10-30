import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from voice_meter import GENRE_COLORS,levels,make_patch,PATCH_W,PATCH_H

class TestVoiceMeter(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_COLORS),10)
        for c in GENRE_COLORS.values():
            self.assertEqual(len(c),3)
            self.assertTrue(all(0<=v<=255 for v in c))
    def test_level_tracks_speech(self):
        a=levels([0.0002]*12+[0.22]*12+[0.0002]*12)
        self.assertLess(a[5],0.01)
        self.assertGreater(a[20],0.55)
        self.assertLess(a[-1],0.05)
    def test_frame_dimensions(self):
        for k,c in GENRE_COLORS.items():
            self.assertEqual(len(make_patch(.6,0,c)),PATCH_W*PATCH_H*3,k)
    def test_loudness_increases_pixels(self):
        c=GENRE_COLORS['ai_work']
        quiet=make_patch(0,0,c)
        loud=make_patch(1,0,c)
        self.assertGreater(sum(loud),sum(quiet)+40000)
    def test_frame_determinism(self):
        self.assertEqual(make_patch(.4,10,GENRE_COLORS['career']),make_patch(.4,10,GENRE_COLORS['career']))
    def test_no_network_or_upload_code(self):
        src=(Path(__file__).resolve().parents[1]/'code'/'voice_meter.py').read_text()
        for forbidden in ['requests.', 'urllib.request', 'TikTok API', 'post_video(']:
            self.assertNotIn(forbidden,src)
if __name__=='__main__':unittest.main()
