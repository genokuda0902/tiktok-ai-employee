import unittest
from quality.cycle1313_review_gate import publishable
class GateTest(unittest.TestCase):
    def test_silent_rejected(self):
        self.assertFalse(publishable(dict(video_present=True,audio_present=False,width=1080,height=1920,duration=15),True))
    def test_unapproved_rejected(self):
        self.assertFalse(publishable(dict(video_present=True,audio_present=True,width=1080,height=1920,duration=15),False))
    def test_approved(self):
        self.assertTrue(publishable(dict(video_present=True,audio_present=True,width=1080,height=1920,duration=15),True))
if __name__=="__main__":unittest.main()
