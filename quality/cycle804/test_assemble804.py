"""Static contract tests; no network, payment, publishing or model downloads."""
import unittest
from assemble804 import GENRES,CAPTIONS
class Cycle804Tests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),len(set(GENRES)))
        self.assertEqual(len(GENRES),10)
    def test_business_genre(self): self.assertIn('sales_business',GENRES)
    def test_eight_japanese_captions(self):
        self.assertEqual(len(CAPTIONS),8)
        self.assertTrue(all(any('\u3040'<=c<='\u9fff' for c in line) for line in CAPTIONS))
    def test_unique_captions(self): self.assertEqual(len(CAPTIONS),len(set(CAPTIONS)))
    def test_no_urls_or_personal_data(self):
        self.assertFalse(any('http' in s or '@' in s for s in CAPTIONS))
if __name__=='__main__': unittest.main()
