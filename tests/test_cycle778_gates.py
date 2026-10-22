import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'video_engine'/'quality'))
from cycle778_hook import *
def fixture():
 return dict(genre=list(GENRES)[0],supported_genres=list(GENRES),
  monthly_sales=list(MONTHS),total_yen=sum(MONTHS),
  source_rights='unverified_review_only',audio_rights='unverified_review_only',
  quality_approved=False,publication_approved=False,manual_post_only=True,
  performance_claim=None,new_assets='original_graphics_plus_inherited_robot')
class Gates(unittest.TestCase):
 def test_valid(self):self.assertTrue(validate(fixture()))
 def test_all_genres(self):
  for g in GENRES:
   m=fixture();m['genre']=g;self.assertTrue(validate(m))
 def test_total(self):
  m=fixture();m['total_yen']=123
  with self.assertRaises(ValueError):validate(m)
 def test_rights(self):
  m=fixture();m['audio_rights']='approved'
  with self.assertRaises(ValueError):validate(m)
 def test_publication(self):
  m=fixture();m['publication_approved']=True
  with self.assertRaises(ValueError):validate(m)
 def test_auto_post(self):
  m=fixture();m['manual_post_only']=False
  with self.assertRaises(ValueError):validate(m)
