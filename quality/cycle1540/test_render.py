import unittest
from pathlib import Path
from render import build

class RenderTests(unittest.TestCase):
    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            build(Path('/no/such/source.mp4'),Path('/tmp/no.mp4'))
    def test_no_automatic_publication(self):
        s = Path(__file__).with_name('render.py').read_text()
        self.assertNotIn('upload_to_tiktok',s)
        self.assertIn('map',s)

if __name__ == '__main__':
    unittest.main()
