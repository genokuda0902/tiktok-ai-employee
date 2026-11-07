"""Fail-closed audio capability validation shared by all video genres."""
from dataclasses import dataclass

@dataclass(frozen=True)
class MediaQA:
    audio_stream: bool
    japanese_narration_verified: bool
    captions_synced: bool
    assets_approved: bool
    human_approved: bool

    @property
    def posting_allowed(self) -> bool:
        return all((self.audio_stream, self.japanese_narration_verified,
                    self.captions_synced, self.assets_approved, self.human_approved))


def test_silent_video_blocked():
    assert not MediaQA(False, False, False, True, True).posting_allowed


def test_audio_stream_alone_insufficient():
    assert not MediaQA(True, False, True, True, True).posting_allowed


def test_human_approval_required():
    assert not MediaQA(True, True, True, True, False).posting_allowed

# cycle1282: local MP4 1080x1920 / 12s / silent, NOT APPROVED.
# espeak -v ja failed: 'Failed to read voice ja'.
# This is a safety test, not a narration implementation or CI success.
