import unittest
from unittest.mock import patch
from tools.cycle1340_media_qa import check

class MediaGateTests(unittest.TestCase):
    @patch("tools.cycle1340_media_qa.subprocess.run")
    @patch("tools.cycle1340_media_qa.probe")
    def test_silent_rejected(self, probe, run):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"15"}}
        run.return_value.returncode=0
        self.assertIn("audio_missing",check("example.mp4")["issues"])
    @patch("tools.cycle1340_media_qa.subprocess.run")
    @patch("tools.cycle1340_media_qa.probe")
    def test_audio_video_passes_metadata_gate(self, probe, run):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"15"}}
        run.return_value.returncode=0
        self.assertTrue(check("example.mp4")["passed"])
if __name__=="__main__":unittest.main()
