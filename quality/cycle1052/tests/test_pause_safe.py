import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pause_safe import GENRES,schedule,require_review_approval,SFX_DURATION,MAX_SHIFT

class PauseSafeTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertEqual(schedule((0.9,),[(0.8,1.1)],genre,2)[0]["status"],"PAUSE_PLACED")
    def test_no_pause_fail_closed(self):
        self.assertEqual(schedule((0.9,),[],duration=2)[0]["status"],"SUPPRESSED_NO_SAFE_PAUSE")
    def test_too_far(self):
        self.assertEqual(schedule((1.0,),[(1.5,1.8)],duration=2)[0]["status"],"SUPPRESSED_NO_SAFE_PAUSE")
    def test_20_3_speech_guard(self):
        self.assertEqual(schedule((20.3,),[(20.687,21.095)],duration=23)[0]["status"],"SUPPRESSED_NO_SAFE_PAUSE")
    def test_inside_pause(self):
        e=schedule((1.0,),[(0.9,1.12)],duration=2)[0]
        self.assertGreaterEqual(e["cue_center_s"]-SFX_DURATION/2,e["pause_s"][0])
        self.assertLessEqual(e["cue_center_s"]+SFX_DURATION/2,e["pause_s"][1])
    def test_max_shift(self):
        e=schedule((1.0,),[(1.08,1.34)],duration=2)[0]
        self.assertLessEqual(abs(e["shift_s"]),MAX_SHIFT)
    def test_bad_genre(self):
        with self.assertRaises(ValueError):schedule((.9,),[(.8,1.1)],"invalid",2)
    def test_bad_boundaries(self):
        with self.assertRaises(ValueError):schedule((1.,.8),[(.5,1.5)],duration=2)
    def test_publish_block(self):
        with self.assertRaises(PermissionError):require_review_approval()
if __name__=="__main__":unittest.main()
