import unittest
from unittest.mock import patch
import json
from quality.cycle1557.media_qa import inspect
class TestQuality(unittest.TestCase):
    @patch("quality.cycle1557.media_qa.subprocess.run")
    def test_effects_do_not_count_as_narration(self,run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"r_frame_rate":"24/1"},{"codec_type":"audio"}],"format":{"duration":"12"}})
        self.assertFalse(inspect("demo.mp4")["publication_approved"])
    @patch("quality.cycle1557.media_qa.subprocess.run")
    def test_explicit_approval_required(self,run):
        run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"r_frame_rate":"24/1"},{"codec_type":"audio"}],"format":{"duration":"12"}})
        self.assertFalse(inspect("demo.mp4",narration_verified=True,caption_sync_verified=True,rights_approved=True)["publication_approved"])
if __name__=="__main__":unittest.main()
