"""Cycle693 numeric, narration and fail-closed contract tests."""
import sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent))
import native_ja_proof as p
class TestCycle693(unittest.TestCase):
 def test_four_month_sum(self):self.assertEqual(sum(p.VALUES),650)
 def test_wrong_example_not_truth(self):self.assertNotEqual(455,sum(p.VALUES))
 def test_native_japanese_lines(self):
  self.assertEqual(len(p.SCENES),4)
  self.assertTrue(all(any(ord(c)>127 for c in voice) for _,voice in p.SCENES))
 def test_no_unverified_speed_claim(self):
  self.assertNotIn("10倍",str(p.SCENES))
  self.assertNotIn("数分で",str(p.SCENES))
 def test_missing_tts_fails_closed(self):
  with patch.object(p.shutil,"which",return_value=None):
   with self.assertRaisesRegex(RuntimeError,"FAIL_CLOSED"):p.build("/tmp/cycle693-should-not-write")
if __name__=="__main__":unittest.main()
