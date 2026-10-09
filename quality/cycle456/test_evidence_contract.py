import unittest
from evidence_contract import validate_evidence

ROWS = [{"id": "D-201", "status": "対応済"},
        {"id": "D-203", "status": "未対応"},
        {"id": "D-206", "status": "未対応"}]
IDS = ["D-203", "D-206"]
CAPTION = "D-203 と D-206 の2件を抽出"
def manifest():
    return dict(rights="SYNTHETIC_ORIGINAL", publication="NOT_APPROVED",
                auto_post=False, voice_verified_japanese=False,
                caption_voice_sync_verified=False)
class TestEvidenceContract(unittest.TestCase):
    def test_missing_voice(self):
        self.assertEqual(validate_evidence(ROWS, IDS, CAPTION, manifest()),
                         "REVIEW_ONLY_NARRATION_MISSING")
    def test_sync_gate(self):
        m = manifest(); m["voice_verified_japanese"] = True
        self.assertEqual(validate_evidence(ROWS, IDS, CAPTION, m),
                         "REVIEW_ONLY_SYNC_UNVERIFIED")
    def test_human_gate(self):
        m = manifest(); m.update(voice_verified_japanese=True, caption_voice_sync_verified=True)
        self.assertEqual(validate_evidence(ROWS, IDS, CAPTION, m), "HUMAN_REVIEW_REQUIRED")
    def test_bad_ids(self):
        with self.assertRaises(ValueError):
            validate_evidence(ROWS, ["D-203"], CAPTION, manifest())
    def test_caption_mismatch(self):
        with self.assertRaises(ValueError):
            validate_evidence(ROWS, IDS, "未対応が2件", manifest())
    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            validate_evidence(ROWS + [ROWS[0]], IDS, CAPTION, manifest())
    def test_unknown_rights(self):
        m = manifest(); m["rights"] = "UNKNOWN"
        with self.assertRaises(ValueError):
            validate_evidence(ROWS, IDS, CAPTION, m)
    def test_approved_block(self):
        m = manifest(); m["publication"] = "APPROVED"
        with self.assertRaises(ValueError):
            validate_evidence(ROWS, IDS, CAPTION, m)
    def test_autopost_block(self):
        m = manifest(); m["auto_post"] = True
        with self.assertRaises(ValueError):
            validate_evidence(ROWS, IDS, CAPTION, m)

if __name__ == "__main__":
    unittest.main()
