"""Fail-closed narration and caption QA, shared across ten genres."""
from dataclasses import dataclass
from hook import GENRES

@dataclass(frozen=True)
class QAResult:
    genre: str
    video_seconds: float
    captions: tuple
    narration_present: bool
    narration_transcript_verified: bool
    audio_caption_sync_verified: bool
    rights_approved: bool

    def evaluate(self):
        if self.genre not in GENRES or not 15 <= self.video_seconds <= 25:
            raise ValueError('genre or duration invalid')
        last = 0.0
        for start,end,text in self.captions:
            if start < last-0.001 or end <= start or end > self.video_seconds+.01:
                raise ValueError('invalid caption intervals')
            if not text.strip() or len(text) > 45:
                raise ValueError('unreadable caption')
            last = end
        blockers=[]
        if not self.narration_present: blockers.append('JAPANESE_NARRATION_ABSENT')
        if not self.narration_transcript_verified: blockers.append('TRANSCRIPT_UNVERIFIED')
        if not self.audio_caption_sync_verified: blockers.append('AUDIO_CAPTION_SYNC_UNVERIFIED')
        if not self.rights_approved: blockers.append('RIGHTS_UNVERIFIED')
        return {'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED',
                'blockers':blockers,'technical_caption_intervals':'PASS'}
