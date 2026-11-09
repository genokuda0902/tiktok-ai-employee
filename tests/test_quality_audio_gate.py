import unittest
from unittest.mock import patch
from src.quality_audio_gate import inspect

class QualityGateTests(unittest.TestCase):
    def test_silent_video_rejected(self):
        import json
        probe = {"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"15"}}
        with patch("subprocess.run") as run:
            run.return_value.stdout=json.dumps(probe)
            run.return_value.returncode=0
            self.assertIn("missing_audio",inspect("test.mp4")["issues"])
    def test_video_with_audio_passes(self):
        import json
        probe = {"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"15"}}
        with patch("subprocess.run") as run:
            run.return_value.stdout=json.dumps(probe)
            run.return_value.returncode=0
            self.assertTrue(inspect("test.mp4")["approved"])

if __name__ == "__main__":
    unittest.main()
