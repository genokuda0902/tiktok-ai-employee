import unittest
from types import SimpleNamespace
from quality.cycle465.voice_evidence_gate import assess_readiness

def b(a,z,c="字幕",s="読み上げ"):
    return SimpleNamespace(start=a,end=z,caption=c,spoken=s)

class TestGate(unittest.TestCase):
    def test_effects_only_is_not_speech(self):
        r=assess_readiness([b(0,1),b(1,20)],20,voice_generated=False,human_listened=False,rights_verified=True)
        self.assertFalse(r["approved_for_review"])
        self.assertFalse(r["approved_for_publication"])
    def test_bad_timing(self):
        r=assess_readiness([b(0,2),b(2,20)],20,voice_generated=True,human_listened=True,rights_verified=True)
        self.assertIn("HOOK_OUTSIDE_1_5S",r["issues"])
    def test_rights_fail_closed(self):
        r=assess_readiness([b(0,1),b(1,20)],20,voice_generated=True,human_listened=True,rights_verified=False)
        self.assertFalse(r["approved_for_review"])
    def test_empty_script(self):
        r=assess_readiness([b(0,1,s=""),b(1,20)],20,voice_generated=True,human_listened=True,rights_verified=True)
        self.assertIn("EMPTY_CAPTION_OR_SCRIPT",r["issues"])
