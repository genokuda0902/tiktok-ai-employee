import unittest
from pathlib import Path
import voice_recovery as v
class TestVoiceRecovery(unittest.TestCase):
 def test_duration(self):self.assertEqual(sum(round(t*30) for t,_ in v.SCENES),600)
 def test_eight_scenes(self):self.assertEqual(len(v.SCENES),8)
 def test_no_private_data(self):self.assertTrue(all(isinstance(line,str) for _,line in v.SCENES))
 def test_japanese(self):self.assertTrue(all(line.endswith("。") for _,line in v.SCENES[1:]))
 def test_fail_closed(self):self.assertIn("raise RuntimeError",Path(v.__file__).read_text())
if __name__=="__main__":unittest.main()
