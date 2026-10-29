import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_wipe import GENRES,validate_config,feather_mask,compose_wipe
class Tests(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(GENRES),10)
 def test_unreviewed_fails_closed(self):
  with self.assertRaises(ValueError): validate_config(1080,1920,30,691,[175],'travel')
 def test_synthetic_other_genre(self):
  validate_config(1080,1920,30,691,[175],'travel',True)
 def test_invalid_cuts(self):
  with self.assertRaises(ValueError): validate_config(1080,1920,30,691,[261,175],'ai_work')
 def test_cuts_too_close(self):
  with self.assertRaises(ValueError): validate_config(1080,1920,30,691,[175,178],'ai_work')
 def test_feather_monotone(self):
  a=feather_mask(100,.5)
  self.assertTrue(np.all(np.diff(a)<=.0001))
 def test_progress(self):
  self.assertGreater(feather_mask(100,.8).sum(),feather_mask(100,.2).sum())
 def test_protected_caption(self):
  old=np.zeros((200,120,3),dtype=np.uint8);new=np.full_like(old,255)
  old[120:]=23;new[120:]=77
  for p in (.1,.4,.6,.9):
   x=compose_wipe(old,new,p,10,110)
   self.assertTrue(np.array_equal(x[120:],old[120:] if p<.5 else new[120:]))
 def test_artwork_changes(self):
  old=np.zeros((200,120,3),np.uint8);new=np.full_like(old,255)
  self.assertGreater(compose_wipe(old,new,.7,10,110)[10:110].mean(),
                     compose_wipe(old,new,.3,10,110)[10:110].mean())
 def test_mismatched_frames(self):
  with self.assertRaises(ValueError):
   compose_wipe(np.zeros((20,20,3),np.uint8),np.zeros((10,20,3),np.uint8),.5,2,15)
if __name__=='__main__': unittest.main()
