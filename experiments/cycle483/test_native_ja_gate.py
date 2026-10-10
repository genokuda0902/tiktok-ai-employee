"""No speech synthesis required for these policy regression tests."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("native_ja_gate",ROOT/"native_ja_gate.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class TestCycle483(unittest.TestCase):
    def test_missing_approval_blocks_publication(self):
        self.assertFalse(mod.approval_gate({}))
    def test_sfx_only_blocks_publication(self):
        self.assertFalse(mod.approval_gate({"full_decode":"PASS","native_ja_voice":"NOT_ACHIEVED"}))
    def test_unreviewed_audio_blocks_publication(self):
        self.assertFalse(mod.approval_gate({"full_decode":"PASS","native_ja_voice":"GENERATED_UNREVIEWED","voice_caption_sync":"SCENE_BOUNDARY_ONLY_UNREVIEWED"}))
    def test_approved_audio_and_video_gate(self):
        qa={"full_decode":"PASS","native_ja_voice":"GENERATED_UNREVIEWED",
            "voice_caption_sync":"SCENE_BOUNDARY_ONLY_UNREVIEWED",
            "human_listening_approved":True,"human_visual_approved":True}
        self.assertTrue(mod.approval_gate(qa))
    def test_no_empty_text(self):
        with self.assertRaises(ValueError):mod.synthesize("  ","/tmp/should_not_exist.wav")
    def test_preflight_structured(self):
        p=mod.preflight()
        self.assertIn("ready",p)
        self.assertIn("voice",p)
        self.assertIsInstance(p["ready"],bool)
if __name__=="__main__":unittest.main()
