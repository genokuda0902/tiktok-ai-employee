import unittest
from quality.cycle1624_review import caption_manifest, validate_captions

class TestReview(unittest.TestCase):
    def test_contiguous(self):
        validate_captions(caption_manifest())
    def test_reject_gap(self):
        caps = caption_manifest()
        caps[1]["start"] = 5
        with self.assertRaises(AssertionError):
            validate_captions(caps)
    def test_reject_missing_text(self):
        caps = caption_manifest()
        caps[0]["text"] = ""
        with self.assertRaises(AssertionError):
            validate_captions(caps)

if __name__ == "__main__":
    unittest.main()
