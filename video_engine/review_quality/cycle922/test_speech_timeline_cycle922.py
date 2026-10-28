import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('s', Path(__file__).with_name('speech_timeline_cycle922.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

class SpeechTimelineTests(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(s.GENRES),10)
    def test_bounds(self):
        self.assertEqual(len(s.SCENE_BOUNDS),9)
        self.assertEqual(s.SCENE_BOUNDS[-1],691)
        self.assertEqual(s.scene_index(0),0)
        self.assertEqual(s.scene_index(690),7)
    def test_bounds_reject(self):
        for f in [-1,691]:
            with self.assertRaises(ValueError):s.scene_index(f)
    def test_scene_coverage(self):
        bits=[True]*800
        self.assertEqual(s.speech_coverage(bits),[1.0]*8)
    def test_empty_vad_fails(self):
        with self.assertRaises(ValueError):s.speech_coverage([])
    def test_silence_fails_gate(self):
        ratios=s.speech_coverage([False]*800)
        self.assertTrue(any(x < .25 for x in ratios))
    def test_smooth_removes_spike(self):
        self.assertFalse(s.smooth_vad([False,False,True,False,False],1)[2])
    def test_time_to_vad_index(self):
        self.assertEqual(s.time_to_vad_index(90),100)
    def test_preserves_caption_text(self):
        y0,y1=s.render_safe_region()
        self.assertGreater(y0,1680)
        self.assertLess(y1,1850)
    def test_reject_publish_filename(self):
        with self.assertRaises(ValueError):s.assert_review_only('ai_work','public.mp4')
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):s.assert_review_only('unknown','x_REVIEW_ONLY.mp4')
    def test_no_posting(self):
        self.assertIn('PUBLICATION_NOT_APPROVED',s.REVIEW_STATUS)
    def test_no_speech_transcription_claim(self):
        self.assertNotIn('transcrib',s.generate.__doc__ or '')

if __name__=='__main__':unittest.main()
