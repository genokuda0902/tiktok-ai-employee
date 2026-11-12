import unittest
from speech_gate import publication_gate

class GateTests(unittest.TestCase):
    def test_aac_silence_is_not_speech(self):
        streams={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}
        result=publication_gate({},streams)
        self.assertFalse(result["posting_allowed"])
        self.assertIn("japanese_narration_unverified",result["issues"])
    def test_missing_audio_fails(self):
        result=publication_gate({"japanese_narration_verified":True},{"streams":[{"codec_type":"video","width":1080,"height":1920}]})
        self.assertIn("audio_track_missing",result["issues"])
    def test_approval_is_required(self):
        data={"japanese_narration_verified":True,"caption_sync_verified":True,"asset_rights_approved":True}
        p={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertIn("employee_approval_missing",publication_gate(data,p)["issues"])

if __name__=="__main__": unittest.main()
