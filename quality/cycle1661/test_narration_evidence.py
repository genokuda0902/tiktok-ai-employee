import unittest
from unittest.mock import patch
import json
import tempfile
from pathlib import Path
from narration_evidence import verify


class EvidenceTests(unittest.TestCase):
    def run_case(self, evidence, streams):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "evidence.json"
            p.write_text(json.dumps(evidence), encoding="utf-8")
            with patch("narration_evidence.subprocess.check_output", return_value=json.dumps({"streams": streams})):
                return verify(Path(d) / "review.mp4", p)

    def test_effect_sound_cannot_pass(self):
        e = dict(audio_kind="sound_effects", transcript_ja="", speech_reviewed_by_human=False,
                 subtitle_sync_reviewed_by_human=False, assets_approved=False, employee_approved=False)
        self.assertFalse(self.run_case(e, [{"codec_type": "audio"}])["publication_approved"])

    def test_audio_missing_even_with_approval(self):
        e = dict(audio_kind="japanese_narration", transcript_ja="確認しました",
                 speech_reviewed_by_human=True, subtitle_sync_reviewed_by_human=True,
                 assets_approved=True, employee_approved=True)
        self.assertIn("missing_audio_stream", self.run_case(e, [])["problems"])

    def test_all_evidence_required(self):
        e = dict(audio_kind="japanese_narration", transcript_ja="確認しました",
                 speech_reviewed_by_human=True, subtitle_sync_reviewed_by_human=True,
                 assets_approved=True, employee_approved=True)
        self.assertTrue(self.run_case(e, [{"codec_type": "audio"}])["publication_approved"])


if __name__ == "__main__":
    unittest.main()
