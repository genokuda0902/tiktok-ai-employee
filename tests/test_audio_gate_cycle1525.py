import unittest
from unittest.mock import patch
import json
from qa.audio_gate import inspect
class GateTests(unittest.TestCase):
 def test_silent_track_not_narration(self):
  probe={'streams':[{'codec_type':'video','width':720,'height':1280},{'codec_type':'audio','codec_name':'aac'}],'format':{'duration':'12'}}
  with patch('subprocess.check_output',return_value=json.dumps(probe)):
   result=inspect('demo.mp4')
   self.assertFalse(result['posting_allowed'])
   self.assertIn('japanese_narration_unverified',result['issues'])
 def test_missing_audio(self):
  probe={'streams':[{'codec_type':'video','width':720,'height':1280}],'format':{'duration':'8'}}
  with patch('subprocess.check_output',return_value=json.dumps(probe)):
   self.assertIn('audio_missing',inspect('demo.mp4')['issues'])
if __name__=='__main__': unittest.main()
