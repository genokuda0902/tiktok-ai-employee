import unittest
from src.quality.audio_evidence_cycle1563 import narration_ready, publication_ready

class AudioEvidenceTest(unittest.TestCase):
    def test_silent_aac_is_not_narration(self):
        self.assertFalse(narration_ready({"streams":[{"codec_type":"audio","codec_name":"aac"}]}))
    def test_all_evidence_required(self):
        p={"streams":[{"codec_type":"audio"}]}
        self.assertTrue(narration_ready(p,True,True))
        self.assertFalse(publication_ready(p,{"transcript_verified":True,"caption_sync_verified":True,"asset_rights_approved":True}))

if __name__=="__main__": unittest.main()
