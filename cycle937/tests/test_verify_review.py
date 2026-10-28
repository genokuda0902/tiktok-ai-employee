import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from verify_review import validate_meta
class MetaTests(unittest.TestCase):
 def good(self):return {'streams':[{'codec_type':'video','codec_name':'h264','width':1080,'height':1920,'r_frame_rate':'30/1'}, {'codec_type':'audio','codec_name':'aac','sample_rate':'48000'}], 'format':{'duration':'23.033333'}}
 def test_good(self):self.assertEqual(len(validate_meta(self.good())),2)
 def test_reject_silent(self):
  d=self.good();d['streams'].pop()
  with self.assertRaises(AssertionError):validate_meta(d)
 def test_reject_wrong_resolution(self):
  d=self.good();d['streams'][0]['width']=720
  with self.assertRaises(AssertionError):validate_meta(d)
 def test_reject_wrong_sample_rate(self):
  d=self.good();d['streams'][1]['sample_rate']='44100'
  with self.assertRaises(AssertionError):validate_meta(d)
 def test_reject_short_video(self):
  d=self.good();d['format']['duration']='10'
  with self.assertRaises(AssertionError):validate_meta(d)
