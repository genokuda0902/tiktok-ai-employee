import unittest,json
from unittest.mock import patch
from quality_gate import inspect
class GateTests(unittest.TestCase):
 def run_gate(self,audio=False,**flags):
  streams=[{"codec_type":"video","width":720,"height":1280,"codec_name":"h264"}]
  if audio: streams.append({"codec_type":"audio","codec_name":"aac"})
  class Result:
   returncode=0;stderr='';stdout=json.dumps({"streams":streams,"format":{"duration":"12"}})
  with patch("subprocess.run",return_value=Result()):
   return inspect("demo.mp4",**flags)
 def test_no_audio_fails(self):
  r=self.run_gate(narration_verified=True,subtitles_verified=True,rights_approved=True,human_approved=True)
  self.assertFalse(r["publication_approved"])
 def test_audio_not_speech_proof(self):
  r=self.run_gate(audio=True,subtitles_verified=True,rights_approved=True,human_approved=True)
  self.assertFalse(r["checks"]["japanese_narration_verified"])
 def test_rights_gate(self):
  r=self.run_gate(audio=True,narration_verified=True,subtitles_verified=True,human_approved=True)
  self.assertFalse(r["publication_approved"])
if __name__=="__main__": unittest.main()
