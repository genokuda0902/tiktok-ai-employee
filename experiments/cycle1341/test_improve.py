import unittest
from pathlib import Path
from improve import build

class TestVisualGuidance(unittest.TestCase):
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            build(Path('/not-present-review.mp4'),Path('/tmp/out.mp4'))

    def test_no_external_assets(self):
        source=Path(__file__).with_name('improve.py').read_text()
        self.assertNotIn('http://',source)
        self.assertNotIn('https://',source)

if __name__ == '__main__':
    unittest.main()
