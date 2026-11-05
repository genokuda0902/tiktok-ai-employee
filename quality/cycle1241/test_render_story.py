import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from render_story import SCENES, create_frames

class StoryTest(unittest.TestCase):
    def test_three_stages(self):
        self.assertEqual([s[2] for s in SCENES],["BEFORE","ACTION","AFTER"])
    def test_frames(self):
        with TemporaryDirectory() as d:
            files=create_frames(d)
            self.assertEqual(len(files),3)
            self.assertTrue(all(Path(p).stat().st_size>0 for p in files))
if __name__=="__main__": unittest.main()
