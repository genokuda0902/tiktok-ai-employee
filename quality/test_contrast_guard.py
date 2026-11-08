import unittest
from contrast_guard import contrast,validate_slide
class ContrastGuardTests(unittest.TestCase):
    def test_high_contrast(self):
        self.assertGreater(contrast((255,255,255),(6,18,35)),7)
    def test_safe_area(self):
        self.assertTrue(validate_slide((255,255,255),(6,18,35),1065))
        self.assertFalse(validate_slide((255,255,255),(6,18,35),1600))
    def test_low_contrast(self):
        self.assertFalse(validate_slide((100,100,100),(110,110,110),1065))
if __name__=='__main__': unittest.main()
