import unittest
from qa_cycle1665 import check_manifest
class TestGate(unittest.TestCase):
    def test_missing_narration_rejected(self):
        self.assertIn("narration_missing",check_manifest({"width":1080,"height":1920}))
    def test_safe_zone_rejected(self):
        m={"width":1080,"height":1920,"japanese_narration_verified":True,"speech_caption_sync_verified":True,"assets_approved":True,"employee_approved":True,"captions":[{"bottom_y":1700}]}
        self.assertEqual(check_manifest(m),["caption_outside_safe_zone"])
    def test_approved_manifest(self):
        m={"width":1080,"height":1920,"japanese_narration_verified":True,"speech_caption_sync_verified":True,"assets_approved":True,"employee_approved":True,"captions":[{"bottom_y":1500}]}
        self.assertEqual(check_manifest(m),[])
if __name__=="__main__": unittest.main()
