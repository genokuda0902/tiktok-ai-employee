import unittest
from dataclasses import replace
from video_engine.quality_cycle451.hook_proof import ProofHook, validate, hook_state, qa_gates, ROWS

class TestCycle451(unittest.TestCase):
    def test_default(self): self.assertTrue(validate(ProofHook()))
    def test_counts(self): self.assertEqual(hook_state(ProofHook(),1.4)["count"],2)
    def test_first(self): self.assertEqual(hook_state(ProofHook(),0)["move"],0)
    def test_last(self): self.assertGreater(hook_state(ProofHook(),2.4)["move"],0.99)
    def test_voice_gate(self): self.assertIn("JAPANESE_NARRATION_MISSING",qa_gates(ProofHook()))
    def test_publication_gate(self): self.assertIn("PUBLICATION_NOT_APPROVED",qa_gates(ProofHook()))
    def test_wrong_canvas(self):
        with self.assertRaises(ValueError): validate(replace(ProofHook(),width=720))
    def test_bad_rights(self):
        with self.assertRaises(ValueError): validate(replace(ProofHook(),rights="UNKNOWN"))
    def test_auto_post(self):
        with self.assertRaises(ValueError): validate(replace(ProofHook(),auto_post=True))
    def test_bad_ids(self):
        with self.assertRaises(ValueError): validate(replace(ProofHook(),rows=(ROWS[0],ROWS[0])))
    def test_bad_duration(self):
        with self.assertRaises(ValueError): validate(replace(ProofHook(),hook_seconds=3))
    def test_genre_fixture(self):
        p=replace(ProofHook(),rows=(("D-101",True),("D-102",False)))
        self.assertEqual(hook_state(p,1.5)["count"],1)

if __name__=="__main__": unittest.main()
