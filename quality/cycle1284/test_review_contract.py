import unittest
from review_contract import validate

class ReviewContractTest(unittest.TestCase):
    def setUp(self):
        self.data = dict(status="REVIEW_ONLY", posting_allowed=False, audio="absent", captions="SRT", assets="original synthetic graphics only", scenes=4)
    def test_review_only(self):
        self.assertTrue(validate(self.data))
    def test_reject_publication(self):
        self.data["posting_allowed"] = True
        self.assertFalse(validate(self.data))
    def test_reject_missing_metadata(self):
        del self.data["assets"]
        self.assertFalse(validate(self.data))

if __name__ == "__main__":
    unittest.main()
