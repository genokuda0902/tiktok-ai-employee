import unittest
from render import SCENES
class ReviewGate(unittest.TestCase):
 def test_four_scenes(self): self.assertEqual(len(SCENES),4)
 def test_caption_each_scene(self): self.assertTrue(all(title and caption for title,caption in SCENES))
 def test_no_personal_media_paths(self): self.assertFalse(any(".png" in x or ".mp4" in x for scene in SCENES for x in scene))
if __name__=="__main__": unittest.main()
