import unittest
from cycle1215_chapter_cues import filtergraph
class TestChapters(unittest.TestCase):
 def test_three(self): self.assertEqual(filtergraph().count("drawtext="),3)
 def test_bad_time(self):
  with self.assertRaises(ValueError): filtergraph([(8,7,"bad")])
 def test_bad_label(self):
  with self.assertRaises(ValueError): filtergraph([(1,2,"a'b")])
if __name__=="__main__": unittest.main()
