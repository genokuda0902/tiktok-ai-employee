"""Reusable, fail-closed numeric proof for ten video genres.

Do not treat arithmetic correctness as proof of narration, caption sync,
source rights, human approval, or publishability.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class NumericProof:
    inputs: tuple[int, ...]
    displayed_total: int
    has_japanese_audio: bool = False
    captions_synced: bool = False
    human_approved: bool = False

    def verify(self) -> dict:
        actual = sum(self.inputs)
        arithmetic_ok = actual == self.displayed_total
        return {
            "arithmetic_ok": arithmetic_ok,
            "expected_total": actual,
            "displayed_total": self.displayed_total,
            "publication_allowed": (
                arithmetic_ok and self.has_japanese_audio
                and self.captions_synced and self.human_approved
            ),
        }
