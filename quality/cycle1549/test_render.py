import unittest
from render import CAPTIONS,srt_text
class TestCaptions(unittest.TestCase):
 def test_four_segments(self): self.assertEqual(srt_text().count("-->"),4)
 def test_japanese_content(self): self.assertIn("SUM関数",srt_text())
 def test_12_second_timeline(self): self.assertEqual(CAPTIONS[-1][1],"00:00:12,000")
if __name__=="__main__":unittest.main()
