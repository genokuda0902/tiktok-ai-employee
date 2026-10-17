import unittest
from PIL import Image
from quality_cycle656.aspect_caption import fit_artwork

class RatioTests(unittest.TestCase):
    def test_ratio(self):
        im = Image.new('RGB', (940, 590))
        out = fit_artwork(im)
        self.assertLess(abs(im.width/im.height-out.width/out.height), 0.004)
