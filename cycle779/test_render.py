import unittest
from render import ass_text, timestamp

class RendererTests(unittest.TestCase):
    def test_eight_cues(self):
        self.assertEqual(ass_text().count('Dialogue:'), 8)
    def test_japanese(self):
        self.assertIn('合計65万円', ass_text())
    def test_font(self):
        self.assertIn('Noto Sans CJK JP', ass_text())
    def test_time(self):
        self.assertEqual(timestamp(12.09), '0:00:12.09')

if __name__ == '__main__':
    unittest.main()
