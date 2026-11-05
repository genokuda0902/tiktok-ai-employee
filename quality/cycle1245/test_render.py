import unittest
from render import SCENES
class StoryTest(unittest.TestCase):
 def test_three_distinct_scenes(self): self.assertEqual(len({s[0] for s in SCENES}),3)
 def test_all_scenes_have_caption(self): self.assertTrue(all(len(s[1])>5 for s in SCENES))
if __name__=="__main__":unittest.main()
