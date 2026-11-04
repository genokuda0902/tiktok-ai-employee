import unittest
from src.cycle1218_visual_beats import make_filter

class TestVisualBeats(unittest.TestCase):
    def test_three_beats(self):
        self.assertEqual(make_filter().count("drawbox="), 3)
    def test_reject_overlap(self):
        with self.assertRaises(ValueError):
            make_filter(((1,3,"red"),(2,4,"blue")))
    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            make_filter(((-1,2,"red"),))
    def test_has_timed_enable(self):
        self.assertIn("between(t,4,5.5)",make_filter())

if __name__=="__main__":
    unittest.main()
