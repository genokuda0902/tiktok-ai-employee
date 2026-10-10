import unittest, pathlib, json, wave
from japanese_tts import LINES
class T(unittest.TestCase):
 def test_six(self):self.assertEqual(len(LINES),6)
 def test_japanese(self):self.assertTrue(all(any(ord(c)>0x3000 for c in x) for x in LINES))
 def test_output(self):
  p=pathlib.Path("output/cycle476/native_ja_narration.wav")
  self.assertTrue(p.is_file())
  with wave.open(str(p)) as w:
   self.assertGreater(w.getnframes()/w.getframerate(),17.8)
 def test_safety(self):
  q=json.loads(pathlib.Path("output/cycle476/voice_qa.json").read_text())
  self.assertFalse(q["auto_post"])
  self.assertEqual(q["publication"],"NOT_APPROVED")
if __name__=="__main__":unittest.main()
