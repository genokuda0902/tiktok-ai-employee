import sys,unittest
from pathlib import Path
from PIL import ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cinematic_prompt as c
class TestCycle916(unittest.TestCase):
 def test_validate(self):self.assertTrue(c.validate())
 def test_genres(self):self.assertEqual(len(c.GENRES),10)
 def test_safe_geometry(self):self.assertEqual((c.W,c.H,c.START,c.FRAMES,c.Y0),(1080,1160,261,87,300))
 def test_render_all_genres(self):
  for genre in c.GENRES:
   self.assertEqual(c.render(45,genre).size,(1080,1160))
 def test_three_stages(self):
  self.assertIsNotNone(ImageChops.difference(c.render(5),c.render(75)).getbbox())
 def test_reject_bad_genre(self):
  with self.assertRaises(ValueError):c.render(1,'invalid')
 def test_reject_bad_frame(self):
  with self.assertRaises(ValueError):c.render(87)
 def test_no_external_requests(self):
  source=Path(c.__file__).read_text()
  self.assertNotIn('requests.',source)
  self.assertNotIn('http://',source)
 def test_review_guard(self):self.assertIn('REVIEW REQUIRED',Path(c.__file__).read_text())
if __name__=='__main__':unittest.main()
