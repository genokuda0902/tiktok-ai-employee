import unittest
from experiments.cycle1388.caption_gate import Segment, DEMO, validate

class TestCaptionGate(unittest.TestCase):
    def test_demo_is_timed_but_not_approved(self):
        self.assertEqual(validate(DEMO,10.8),["narration unverified","employee approval missing"])
    def test_overlapping_captions_fail(self):
        self.assertIn("overlap/out-of-range caption",validate([Segment(0,3,"A"),Segment(2,4,"B")],5,True,True))
    def test_approved_narrated_timing(self):
        self.assertEqual(validate(DEMO,10.8,True,True),[])
if __name__=="__main__": unittest.main()
