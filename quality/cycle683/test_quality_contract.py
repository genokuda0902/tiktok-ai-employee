import unittest
from quality_contract import *
class QualityContractTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(PALETTES),10)
    def test_resolution(self): self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
    def test_safe_graphics(self):
        self.assertTrue(validate_graphic_box((70,620,940,740)))
        with self.assertRaises(ValueError): validate_graphic_box((70,800,940,740))
    def test_manual_review(self):
        self.assertIn("NOT_APPROVED",require_manual_review())
        with self.assertRaises(ValueError): require_manual_review(auto_post=True)
    def test_timeline(self):
        scenes=[{"scene":1,"start":0.0,"end":1.0,"caption_kind":"editorial_not_transcript","spoken_text":"テスト"}]
        self.assertEqual(validate_timeline(scenes),1.0)
if __name__=="__main__": unittest.main()
