import unittest
from gate import inspect

class GateTests(unittest.TestCase):
    def test_missing_file_rejected(self):
        with self.assertRaises(Exception):
            inspect("/no/such/video.mp4")

    def test_fail_closed_source(self):
        import inspect as pyinspect
        source = pyinspect.getsource(inspect)
        self.assertIn('"publication_allowed": False', source)
        self.assertIn('missing_audio', source)
        self.assertIn('human_asset_and_caption_approval_required', source)

if __name__ == "__main__":
    unittest.main()
