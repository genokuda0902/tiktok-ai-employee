import unittest
from quality.cycle1290.media_contract import publication_allowed

class ReviewGateTest(unittest.TestCase):
    def setUp(self):
        self.media={"video":True,"vertical_1080p":True,"audio":True,"duration":12.0}
    def test_silent_blocked(self):
        self.media["audio"]=False
        self.assertFalse(publication_allowed(self.media,True,True,True))
    def test_missing_approval_blocked(self):
        self.assertFalse(publication_allowed(self.media,True,False,True))
    def test_fully_approved(self):
        self.assertTrue(publication_allowed(self.media,True,True,True))
if __name__=="__main__": unittest.main()
