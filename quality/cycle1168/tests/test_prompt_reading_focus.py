import unittest
from prompt_reading_focus import PALETTES,DEFAULT_STEPS,filter_graph,validate,POLICY

class FocusTest(unittest.TestCase):
 def manifest(self):return {'genre':'ai','steps':[dict(s) for s in DEFAULT_STEPS]}
 def test_ten_genres(self):
  self.assertEqual(len(PALETTES),10)
  for genre in PALETTES:
   m=self.manifest();m['genre']=genre
   self.assertEqual(filter_graph(m).count('drawbox='),3)
 def test_order_and_times(self):
  s=DEFAULT_STEPS
  self.assertEqual([x['name'] for x in s],['purpose','condition','format'])
  self.assertTrue(all(s[i]['end']<=s[i+1]['start'] for i in range(2)))
 def test_caption_clearance(self):
  self.assertTrue(all(x['rect'][1]+x['rect'][3]<1240 for x in DEFAULT_STEPS))
 def test_only_three_overlays(self):
  self.assertEqual(filter_graph(self.manifest()).count("enable='between(t,"),3)
 def test_no_unsafe_genre(self):
  with self.assertRaises(KeyError):filter_graph({'genre':'unapproved','steps':DEFAULT_STEPS})
 def test_policy_literal(self):
  self.assertEqual(POLICY,'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED')
