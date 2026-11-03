import unittest
from upper_detail import filtergraph

class TestDetail(unittest.TestCase):
    def test_upper_crop(self):
        self.assertIn('crop=1080:1350:0:0',filtergraph())
    def test_audio_untouched_by_filter(self):
        self.assertNotIn('[0:a]',filtergraph())
    def test_invalid_zone(self):
        with self.assertRaises(AssertionError):
            filtergraph(caption_zone=1920)
    def test_strength_limit(self):
        with self.assertRaises(AssertionError):
            filtergraph(amount=2)

if __name__=='__main__':
    unittest.main()
