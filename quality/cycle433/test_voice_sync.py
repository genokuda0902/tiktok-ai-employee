import unittest
from voice_sync import scene_plan,speed_ratio
class VoiceSyncTests(unittest.TestCase):
 def test_plan(self):self.assertEqual(len(scene_plan({'scenes':[{'voice':'はい','caption':'はい','seconds':2}]})),1)
 def test_missing_voice(self):
  with self.assertRaises(ValueError):scene_plan({'scenes':[{'caption':'はい','seconds':2}]})
 def test_missing_caption(self):
  with self.assertRaises(ValueError):scene_plan({'scenes':[{'voice':'はい','seconds':2}]})
 def test_zero_duration(self):
  with self.assertRaises(ValueError):scene_plan({'scenes':[{'voice':'はい','caption':'はい','seconds':0}]})
 def test_empty_plan(self):
  with self.assertRaises(ValueError):scene_plan({'scenes':[]})
 def test_tempo(self):self.assertAlmostEqual(speed_ratio(2,2.1),1)
 def test_too_fast(self):
  with self.assertRaises(ValueError):speed_ratio(9,2)
 def test_too_slow(self):
  with self.assertRaises(ValueError):speed_ratio(.2,3)
if __name__=='__main__':unittest.main()
