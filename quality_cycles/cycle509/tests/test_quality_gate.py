import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from quality_gate import captions_readable,check_voice_segments,publication_status,SUPPORTED_GENRES
class TestCycle509(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(SUPPORTED_GENRES),10)
 def test_readable(self):self.assertTrue(captions_readable([{'caption':'出典を確認','start':0,'end':1.2}]))
 def test_overlong(self):self.assertFalse(captions_readable([{'caption':'あ'*21,'start':0,'end':3}]))
 def test_too_fast(self):self.assertFalse(captions_readable([{'caption':'あ'*10,'start':0,'end':0.3}]))
 def test_no_voice(self):self.assertFalse(check_voice_segments([],[{'start':0,'end':2}]))
 def test_voice_overflow(self):
  s=[{'scene':0,'engine':'kokoro-ja','text':'日本語','sample_rate':24000,'wav_exists':True,'duration':3.0}]
  self.assertFalse(check_voice_segments(s,[{'start':0,'end':2.5}]))
 def test_voice_valid_machine_only(self):
  s=[{'scene':0,'engine':'kokoro-ja','text':'日本語','sample_rate':24000,'wav_exists':True,'duration':2.0}]
  self.assertTrue(check_voice_segments(s,[{'start':0,'end':2.5}]))
 def test_publication_gate(self):
  self.assertEqual(publication_status({'native_japanese_voice':'BLOCKED','full_decode':'PASS','resolution':[1080,1920]}),'NOT_APPROVED')
 def test_no_bypass_without_rights(self):
  q={'native_japanese_voice':'HUMAN_VERIFIED','voice_caption_sync':'PASS','human_review':'APPROVED','full_decode':'PASS','resolution':[1080,1920],'device_playback':'VERIFIED'}
  self.assertEqual(publication_status(q),'NOT_APPROVED')
if __name__=='__main__':unittest.main()
