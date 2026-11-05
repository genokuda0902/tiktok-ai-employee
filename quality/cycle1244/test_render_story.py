import unittest
from render_story import frame
class StoryTest(unittest.TestCase):
    def test_resolution(self): self.assertEqual(frame(0).size,(720,1280))
    def test_scene_changes(self):
        self.assertNotEqual(frame(1).tobytes(),frame(6).tobytes())
        self.assertNotEqual(frame(6).tobytes(),frame(11).tobytes())
if __name__=="__main__": unittest.main()
