import unittest
from scene_contract import Scene, validate, caption_bounds_ok, publication_allowed

BASE = [
    Scene(0, 1.5, "HOOK", "Start", "Start", "Start", "split"),
    Scene(1.5, 4, "BEFORE", "Before", "Before", "Before", "chat"),
    Scene(4, 6, "CONTEXT", "Context", "Context", "Context", "card"),
    Scene(6, 9, "AFTER", "After", "After", "After", "chat"),
    Scene(9, 12, "METHOD", "Method", "Method", "Method", "steps"),
    Scene(12, 15, "EXAMPLE", "Example", "Example", "Example", "chat"),
    Scene(15, 18, "COMPARE", "Compare", "Compare", "Compare", "split"),
    Scene(18, 20, "CTA", "Save", "Save", "Save", "save"),
]
M = dict(asset_rights="ORIGINAL_SYNTHETIC", privacy="NO_REAL_PERSONAL_DATA",
         publication="NOT_APPROVED", auto_post=False,
         narration_status="UNAVAILABLE", quality_status="HUMAN_REVIEW")
class Tests(unittest.TestCase):
    def test_timeline(self): self.assertTrue(validate(BASE, M))
    def test_voice_gate(self): self.assertFalse(publication_allowed(M))
    def test_caption(self): self.assertTrue(caption_bounds_ok((38, 1005, 682, 1115)))
    def test_bad_caption(self): self.assertFalse(caption_bounds_ok((38, 1160, 682, 1210)))
if __name__ == "__main__": unittest.main()
