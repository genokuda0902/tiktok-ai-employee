import unittest
from tts_ci import SENTENCES,GENRES
class ContractTests(unittest.TestCase):
    def test_eight_scenes(self): self.assertEqual(len(SENTENCES),8)
    def test_japanese_content(self): self.assertTrue(all(any('\u3040'<=c<='\u9fff' for c in s) for s in SENTENCES))
    def test_distinct_scenes(self): self.assertEqual(len(set(SENTENCES)),8)
    def test_ten_genres(self): self.assertEqual(len(set(GENRES)),10)
    def test_target_genre(self): self.assertIn('sales_business',GENRES)
    def test_no_private_data(self): self.assertFalse(any('@' in s or 'http' in s for s in SENTENCES))
if __name__=='__main__': unittest.main()
