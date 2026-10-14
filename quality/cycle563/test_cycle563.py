"""Cycle563 offline tests; do not require video assets or paid APIs."""
import unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from build_cycle563 import PAUSES,filter_graph,FPS

def map_frame(n):
    return n+sum(length for at,length in PAUSES if at<=n)

class TimelineTests(unittest.TestCase):
    def test_seven_pauses(self):self.assertEqual(len(PAUSES),7)
    def test_duration_15_6(self):self.assertEqual(375+sum(n for _,n in PAUSES),468)
    def test_fps(self):self.assertEqual(FPS,30)
    def test_speech_not_stretched(self):
        f=filter_graph();self.assertNotIn('rubberband',f);self.assertNotIn('atempo',f)
    def test_audio_pad(self):self.assertEqual(filter_graph().count('apad='),7)
    def test_video_hold(self):self.assertEqual(filter_graph().count('tpad='),7)
    def test_caption_region_untouched(self):self.assertIn('crop=950:680:65:610',filter_graph())
    def test_illustration_only(self):self.assertIn('overlay=65:610',filter_graph())
    def test_map_start(self):self.assertEqual(map_frame(0),0)
    def test_map_end(self):self.assertEqual(map_frame(374),467)
    def test_map_after_first(self):self.assertEqual(map_frame(17),29)
    def test_no_negative_hold(self):self.assertTrue(all(n>0 for _,n in PAUSES))
    def test_increasing_cuts(self):self.assertEqual(sorted(i for i,_ in PAUSES),[i for i,_ in PAUSES])
    def test_ten_genres(self):
        cfg=Path(__file__).parent/'genres.json'
        self.assertEqual(len(json.loads(cfg.read_text(encoding='utf8'))['genres']),10)
if __name__=='__main__':unittest.main()
