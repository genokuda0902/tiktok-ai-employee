import unittest
from unittest.mock import patch
from quality.cycle1487.inspect import inspect

class QualityGateTest(unittest.TestCase):
    @patch("quality.cycle1487.inspect.subprocess.run")
    def test_audio_cue_not_narration(self, run):
        run.return_value.stdout = '{"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}'
        self.assertFalse(inspect("cue.mp4", human_approved=True)["publication_approved"])

    @patch("quality.cycle1487.inspect.subprocess.run")
    def test_all_evidence_required(self, run):
        run.return_value.stdout = '{"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}'
        self.assertTrue(inspect("ok.mp4", True, True, True)["publication_approved"])

if __name__ == "__main__": unittest.main()
