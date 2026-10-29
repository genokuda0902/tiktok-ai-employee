import unittest
from verification_reveal import ART_BOTTOM,GENRES,REVIEWED,artwork,load_verified_source,stage,require_genre,START,END

class TestCrossSceneVerification(unittest.TestCase):
 def test_source_totals_are_derived_not_hardcoded(self):
  data,totals=load_verified_source()
  self.assertEqual(totals,{k:sum(v) for k,v in data.items()})
  self.assertEqual(totals,{'営業A':46,'営業B':29})
 def test_synthetic_draft_is_explicitly_wrong(self):
  _,t=load_verified_source();self.assertEqual(t['営業A']-1,45)
 def test_stages(self):
  self.assertEqual([stage(x) for x in (0,0.29,0.30,0.63,0.64,1)],[0,0,1,1,2,2])
 def test_caption_area(self):
  self.assertEqual(ART_BOTTOM,1240);self.assertEqual((START,END),(435,522))
 def test_image_dimensions(self):
  self.assertEqual(artwork(.9).size,(1080,ART_BOTTOM))
 def test_stage_visuals_differ(self):
  self.assertNotEqual(artwork(.1).tobytes(),artwork(.8).tobytes())
 def test_unreviewed_genres_fail_closed(self):
  self.assertEqual(len(GENRES),10)
  for genre in GENRES:
   if genre not in REVIEWED:
    with self.assertRaises(PermissionError):require_genre(genre)
 def test_unknown_genre_fails(self):
  with self.assertRaises(ValueError):require_genre('fake')
if __name__=='__main__':unittest.main()
