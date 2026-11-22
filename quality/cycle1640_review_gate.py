"""Fail-closed publish gate for ten-topic review renders (stdlib only)."""
from dataclasses import dataclass
import unittest

@dataclass(frozen=True)
class ReviewEvidence:
    video_decodes: bool
    width: int
    height: int
    audio_stream: bool
    japanese_narration_verified: bool
    captions_speech_synced: bool
    assets_approved: bool
    employee_approved: bool

def publication_allowed(e: ReviewEvidence) -> bool:
    return all((
        e.video_decodes, e.width == 1080, e.height == 1920,
        e.audio_stream, e.japanese_narration_verified,
        e.captions_speech_synced, e.assets_approved,
        e.employee_approved
    ))

class QualityGateTests(unittest.TestCase):
    def test_review_only_silent_video_rejected(self):
        e = ReviewEvidence(True, 1080, 1920, False, False, False, True, False)
        self.assertFalse(publication_allowed(e))
    def test_audio_stream_without_verified_speech_rejected(self):
        e = ReviewEvidence(True, 1080, 1920, True, False, True, True, True)
        self.assertFalse(publication_allowed(e))
    def test_unapproved_assets_rejected(self):
        e = ReviewEvidence(True, 1080, 1920, True, True, True, False, True)
        self.assertFalse(publication_allowed(e))
    def test_all_gates_pass(self):
        e = ReviewEvidence(True, 1080, 1920, True, True, True, True, True)
        self.assertTrue(publication_allowed(e))

if __name__ == "__main__":
    unittest.main()
