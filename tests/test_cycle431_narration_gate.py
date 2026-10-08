import tempfile
import unittest
import wave
from pathlib import Path
import importlib.util

MODULE = Path(__file__).resolve().parents[1] / "src/quality/narration_gate.py"
spec = importlib.util.spec_from_file_location("narration_gate", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

GOOD = {"license_status":"APPROVED","synthesized_for_this_video":True,
        "japanese_listening_confirmed":True,"meaning_sync_confirmed":True,
        "auto_post":False}
SEG = [{"start":0.0,"end":1.0,"text":"これはテストです"}]

class NarrationGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.p = Path(self.temp.name) / "voice.wav"
        with wave.open(str(self.p),"wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((int(10000)).to_bytes(2,"little",signed=True)*24000)
    def tearDown(self):
        self.temp.cleanup()
    def check(self, prov=None, seg=None, duration=1.0, path=None):
        return module.inspect_voice(path or self.p, SEG if seg is None else seg,
                                    duration, GOOD if prov is None else prov)
    def test_technical_pass_is_not_publication_approval(self):
        r=self.check();self.assertTrue(r["technical_pass"])
        self.assertEqual(r["publication"],"NOT_APPROVED")
        self.assertTrue(r["human_review_required"])
    def test_missing_file(self):
        self.assertIn("WAV_MISSING",self.check(path=self.p.with_name("missing.wav"))["errors"])
    def test_silent(self):
        with wave.open(str(self.p),"wb") as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000)
            w.writeframes(b"\0\0"*24000)
        self.assertIn("SILENT_OR_TOO_QUIET",self.check()["errors"])
    def test_duration_mismatch(self):
        self.assertIn("DURATION_MISMATCH",self.check(duration=2.0)["errors"])
    def test_empty_caption(self):
        self.assertIn("NO_CAPTIONS",self.check(seg=[])["errors"])
    def test_caption_out_of_range(self):
        self.assertIn("BAD_CAPTION_TIMELINE",self.check(seg=[{"start":0,"end":4,"text":"a"}])["errors"])
    def test_license_missing(self):
        p=dict(GOOD,license_status="UNKNOWN")
        self.assertIn("VOICE_LICENSE_UNVERIFIED",self.check(prov=p)["errors"])
    def test_language_not_listened(self):
        p=dict(GOOD,japanese_listening_confirmed=False)
        self.assertIn("JAPANESE_LISTENING_UNVERIFIED",self.check(prov=p)["errors"])
    def test_semantics_unverified(self):
        p=dict(GOOD,meaning_sync_confirmed=False)
        self.assertIn("SEMANTIC_SYNC_UNVERIFIED",self.check(prov=p)["errors"])
    def test_autopost_rejected(self):
        p=dict(GOOD,auto_post=True)
        self.assertIn("AUTO_POST_NOT_FORBIDDEN",self.check(prov=p)["errors"])
    def test_provenance_rejected(self):
        p=dict(GOOD,synthesized_for_this_video=False)
        self.assertIn("VOICE_PROVENANCE_UNVERIFIED",self.check(prov=p)["errors"])
    def test_empty_text_rejected(self):
        self.assertIn("EMPTY_CAPTION",self.check(seg=[{"start":0,"end":1,"text":""}])["errors"])
if __name__ == "__main__":
    unittest.main()
