import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from focus_overlay import (FRAMES,FOCUS_BOXES,GENRE_COLORS,ass_time,ass_color,validate_boxes,create_ass)

class FocusTests(unittest.TestCase):
 def test_frame_count(self):self.assertEqual(sum(FRAMES),429)
 def test_genres(self):self.assertEqual(len(GENRE_COLORS),10)
 def test_boxes_safe(self):validate_boxes()
 def test_unsafe_box_rejected(self):
  with self.assertRaises(ValueError):validate_boxes(((10,10,100,100),)*8)
 def test_ass_time(self):self.assertEqual(ass_time(429),'0:00:14.30')
 def test_ass_color(self):self.assertEqual(ass_color('35E8D2'),'&H00D2E835')
 def test_ass_events(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=create_ass(Path(tmp)/'focus.ass')
   s=p.read_text();self.assertEqual(s.count('Dialogue:'),16)
   self.assertIn('0:00:14.30',s)
   self.assertIn('\\fad(180,180)',s)
 def test_reject_genre(self):
  with self.assertRaises(ValueError):create_ass('/tmp/unused_focus.ass','bad_genre')
if __name__=='__main__':unittest.main()
