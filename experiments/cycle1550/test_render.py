import unittest
from render import frame,W,H
class TestRenderer(unittest.TestCase):
    def test_dimensions(self):self.assertEqual(frame(0).size,(W,H))
    def test_animation_changes(self):self.assertNotEqual(frame(1).tobytes(),frame(10).tobytes())
    def test_typing_changes(self):self.assertNotEqual(frame(6.1).tobytes(),frame(8).tobytes())
if __name__=="__main__":unittest.main()
