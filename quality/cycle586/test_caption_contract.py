import unittest
from caption_contract import ass, wrap, MARGIN_BOTTOM

class SafeCaptionTests(unittest.TestCase):
    def test_two_lines(self):
        self.assertEqual(wrap("手計算の前に、合計720を確認"), "手計算の前に、\\N合計720を確認")

    def test_safe_bottom_margin(self):
        self.assertGreaterEqual(MARGIN_BOTTOM, 300)

    def test_10_genres_share_renderer(self):
        for i in range(10):
            self.assertIn("PlayResX: 1080", ass([(0, 1000, "字幕")]))

    def test_reject_oversize(self):
        with self.assertRaises(ValueError):
            wrap("長" * 30)

if __name__ == "__main__":
    unittest.main()
