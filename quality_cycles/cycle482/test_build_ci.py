import json, unittest
from pathlib import Path
P=Path(__file__).resolve().parent
class TestCycle482(unittest.TestCase):
 def test_six_original_scenes(self):
  import build_ci
  self.assertEqual(len(build_ci.DATA),6)
 def test_japanese_scripts(self):
  import build_ci
  self.assertTrue(all(len(row[3])>=20 for row in build_ci.DATA))
 def test_video_exists(self):
  self.assertTrue((P/'output'/'cycle482_NATIVE_JAPANESE_HUMAN_REVIEW.mp4').is_file())
 def test_qa(self):
  qa=json.loads((P/'output'/'qa_ci.json').read_text())
  self.assertEqual(qa['resolution'],[1080,1920])
  self.assertEqual(qa['full_decode'],'PASS')
  self.assertEqual(qa['publication'],'NOT_APPROVED')
  self.assertEqual(qa['audio_codec'],'aac')
  self.assertEqual(qa['cost_jpy'],0)
 def test_voice_alignment(self):
  qa=json.loads((P/'output'/'qa_ci.json').read_text())
  self.assertTrue(qa['scene_aligned'])
  self.assertIn('JAPANESE_SYNTHESIZED',qa['narration'])
if __name__=='__main__':unittest.main()
