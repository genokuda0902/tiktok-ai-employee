import unittest
from src.media_truth_gate import evaluate

class MediaTruthGateTests(unittest.TestCase):
    def meta(self, audio=True, width=1080):
        streams = [{"codec_type":"video","codec_name":"h264","width":width,"height":1920}]
        if audio: streams.append({"codec_type":"audio","codec_name":"aac"})
        return {"streams":streams,"format":{"duration":"23.033"}}
    def test_stream_presence_does_not_claim_japanese_speech(self):
        r=evaluate(self.meta())
        self.assertTrue(r["checks"]["audio_present"])
        self.assertFalse(r["checks"]["japanese_speech_verified"])
        self.assertEqual(r["status"],"REVIEW_REQUIRED")
    def test_missing_audio_fails(self):
        self.assertFalse(evaluate(self.meta(audio=False))["checks"]["audio_present"])
    def test_wrong_resolution_fails(self):
        self.assertFalse(evaluate(self.meta(width=720))["checks"]["portrait_1080x1920"])
    def test_explicit_full_review_passes(self):
        r=evaluate(self.meta(),captions_verified=True,japanese_speech_verified=True,
                   privacy_approved=True,visual_reviewed=True)
        self.assertEqual(r["status"],"PASS")

if __name__=="__main__": unittest.main()
