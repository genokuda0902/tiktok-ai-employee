import unittest
from tools.cycle1203_scene_cue import filtergraph

class CueTests(unittest.TestCase):
    def test_default_window(self):
        self.assertIn("between(t,3,6)",filtergraph())
    def test_two_boxes(self):
        self.assertEqual(filtergraph().count("drawbox="),2)
    def test_reject_invalid_window(self):
        with self.assertRaises(ValueError):
            filtergraph(5,5)

if __name__=="__main__":
    unittest.main()
