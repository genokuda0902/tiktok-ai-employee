import unittest
from pathlib import Path

class ReviewTest(unittest.TestCase):
 def test_source_exists(self):
  p=Path(__file__).with_name('render.py')
  self.assertTrue(p.exists())
  text=p.read_text(encoding='utf-8')
  self.assertIn('REVIEW ONLY',text)
  self.assertIn('1080:1920',text)
  self.assertIn('SUM(B2:B4)',text)

if __name__=='__main__': unittest.main()
