import unittest
from review_quality import approved
class TestGate(unittest.TestCase):
    def setUp(self): self.meta={"width":1080,"height":1920,"audio_stream":True}
    def test_audio_not_speech(self): self.assertFalse(approved(self.meta))
    def test_silent(self):
        self.meta["audio_stream"]=False
        self.assertFalse(approved(self.meta,True,True,True,True))
    def test_all_evidence(self): self.assertTrue(approved(self.meta,True,True,True,True))
if __name__=="__main__":unittest.main()
