import unittest
from unittest.mock import patch
from quality_cycle1307 import validate

class ReviewGateTests(unittest.TestCase):
    @patch("quality_cycle1307.subprocess.run")
    @patch("quality_cycle1307.probe")
    def test_silent_video_blocked(self,probe,run):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"15"}}
        run.return_value.returncode=0
        self.assertFalse(validate("demo.mp4",True,True,True,True)["posting_allowed"])
    @patch("quality_cycle1307.subprocess.run")
    @patch("quality_cycle1307.probe")
    def test_unapproved_assets_blocked(self,probe,run):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"15"}}
        run.return_value.returncode=0
        self.assertFalse(validate("demo.mp4",True,True,False,True)["posting_allowed"])
if __name__=="__main__":unittest.main()
