import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import typography_cut as t

class CutTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(t.GENRES),10)
        self.assertEqual(len(set(t.GENRES)),10)
    def test_valid_source(self):
        t.verify_source(dict(width=1080,height=1920,fps='30/1',audio_codec='aac',sample_rate=48000,frames=75))
    def test_bad_resolution(self):
        with self.assertRaises(ValueError): t.verify_source(dict(width=720,height=1280,fps='30/1',audio_codec='aac',sample_rate=48000,frames=75))
    def test_bad_audio(self):
        with self.assertRaises(ValueError): t.verify_source(dict(width=1080,height=1920,fps='30/1',audio_codec='mp3',sample_rate=44100,frames=75))
    def test_short_source(self):
        with self.assertRaises(ValueError): t.verify_source(dict(width=1080,height=1920,fps='30/1',audio_codec='aac',sample_rate=48000,frames=45))
    def test_mask_top(self):
        self.assertEqual(int(t.alpha_mask()[0]),255)
    def test_mask_bottom(self):
        self.assertEqual(int(t.alpha_mask()[-1]),0)
    def test_mask_monotonic(self):
        self.assertTrue(np.all(np.diff(t.alpha_mask().astype(np.int16))<=0))
    def test_invalid_mask(self):
        with self.assertRaises(ValueError): t.alpha_mask(20,40)
    def test_clean_plate(self):
        frame=np.zeros((1920,1080,3),dtype=np.uint8)
        self.assertEqual(t.clean_plate(frame).size,(1080,1170))
    def test_wrong_shape(self):
        with self.assertRaises(ValueError): t.clean_plate(np.zeros((10,10,3),dtype=np.uint8))
    def test_contiguous_cut(self):
        self.assertEqual(t.OLD_END+1,t.NEW_START)
        self.assertLess(t.NEW_END,t.NEW_REFERENCE)
    def test_no_blend_filter(self):
        self.assertNotIn('blend=',t.graph())
    def test_sha_gate(self):
        with self.assertRaises(FileNotFoundError):t.render('/nonexistent.mp4','/tmp/out.mp4','0'*64)

if __name__=='__main__':unittest.main()
