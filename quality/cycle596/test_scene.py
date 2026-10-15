import unittest
from quality.cycle596.proof_contract import GENRES,validate,proof
from quality.cycle596.scene import frame
class TestCycle596(unittest.TestCase):
    def test_math(self):
        self.assertEqual(validate(),720)
        self.assertEqual(frame(0)[1]["partial"],120)
        self.assertEqual(frame(.5)[1]["partial"],270)
        self.assertEqual(frame(1.5)[1]["partial"],720)
    def test_genres(self):
        for g in GENRES:
            img,p=frame(1.5,genre=g)
            self.assertEqual(img.size,(1080,1920))
            self.assertEqual(p["total"],720)
    def test_safe_caption(self):
        self.assertLess(frame(1.5)[1]["caption_box"][3],1536)
        self.assertFalse(proof()["claimed_time_savings"])
    def test_invalid(self):
        for v in ((),(1,2,3),(-1,2,3,4),(1,2,3,10000)):
            with self.assertRaises(ValueError):validate(v)
if __name__=="__main__":unittest.main()
