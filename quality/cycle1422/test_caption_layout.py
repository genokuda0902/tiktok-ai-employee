import unittest
from caption_layout import fit_caption, publication_gate

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

class CaptionTests(unittest.TestCase):
    def test_short_caption(self):
        self.assertEqual(fit_caption("合計 12,400円", FONT), 24)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            fit_caption("", FONT)
    def test_no_approval_is_not_publishable(self):
        self.assertFalse(publication_gate(False, False, True, False))
    def test_all_approvals_required(self):
        self.assertTrue(publication_gate(True, True, True, True))

if __name__ == "__main__":
    unittest.main()
