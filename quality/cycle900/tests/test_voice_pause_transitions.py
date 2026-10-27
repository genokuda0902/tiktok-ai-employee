import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from voice_pause_transitions import (WIDTH,HEIGHT,FPS,CUT_FRAMES,CAPTION_TOP,EFFECT_BOTTOM,
    WINDOW_FRAMES,GENRES,POLICY,gate_cut,active_cut,light_strength,measure_cut_rms)

class TestCutQuality(unittest.TestCase):
    def test_dimensions(self): self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
    def test_ten_unique_genres(self): self.assertEqual(len(set(GENRES)),10)
    def test_review_only(self):
        self.assertFalse(any(POLICY[x] for x in ('publication_approved','automatic_posting','external_upload','paid_service')))
        self.assertTrue(POLICY['human_review_required'])
    def test_caption_safe(self): self.assertLess(EFFECT_BOTTOM,CAPTION_TOP)
    def test_cut_frames(self): self.assertEqual(CUT_FRAMES,tuple(sorted(set(CUT_FRAMES))))
    def test_pause_gate(self): self.assertTrue(gate_cut(.001)); self.assertFalse(gate_cut(.08))
    def test_invalid_rms(self):
        for x in (-.01,1.01):
            with self.assertRaises(ValueError): gate_cut(x)
    def test_active_window(self):
        self.assertEqual(active_cut(89,(89,)),(89,0))
        self.assertIsNone(active_cut(92,(89,)))
    def test_no_cut_outside(self): self.assertIsNone(active_cut(100,()))
    def test_light_bounds(self):
        self.assertGreater(light_strength(0),light_strength(2))
        self.assertEqual(light_strength(WINDOW_FRAMES+1),0.)
    def test_no_audio_semantic_claim(self): self.assertFalse('speech_verified' in POLICY)
    def test_measure_silence(self):
        import numpy as np
        arr=np.zeros(16000*23,dtype=np.float32)
        self.assertTrue(all(v==0 for v in measure_cut_rms(arr,16000).values()))
    def test_duration(self): self.assertLess(max(CUT_FRAMES)/FPS,23.0334)

if __name__=='__main__':unittest.main()
