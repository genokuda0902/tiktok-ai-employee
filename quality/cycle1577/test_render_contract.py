import unittest
from render_contract import SCENES,validate_scenes,publication_approved
class TestRenderContract(unittest.TestCase):
    def test_timeline(self): validate_scenes(SCENES)
    def test_gap_rejected(self):
        with self.assertRaises(AssertionError): validate_scenes([("a","b",0,2),("c","d",3,4)])
    def test_overlap_rejected(self):
        with self.assertRaises(AssertionError): validate_scenes([("a","b",0,2),("c","d",1,4)])
    def test_publication_fail_closed(self):
        self.assertFalse(publication_approved())
        self.assertFalse(publication_approved(True,True,True,False))
        self.assertTrue(publication_approved(True,True,True,True))
if __name__ == "__main__": unittest.main()
