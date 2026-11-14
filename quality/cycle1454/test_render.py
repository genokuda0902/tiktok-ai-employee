import unittest
from render import SCENES
class TestRender(unittest.TestCase):
    def test_scenes(self): self.assertEqual(len(SCENES),4)
    def test_content(self): self.assertTrue(all(a and b for a,b in SCENES))
if __name__=="__main__":unittest.main()
