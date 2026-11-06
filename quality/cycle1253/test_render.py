import unittest
from pathlib import Path
import subprocess
from render import SCENES
class StoryTests(unittest.TestCase):
 def test_three_stages(self):
  self.assertEqual([x[2] for x in SCENES],['BEFORE','ACTION','AFTER'])
 def test_no_personal_data(self):
  self.assertTrue(all('REVIEW ONLY' not in x[0] for x in SCENES))
 def test_ffmpeg_available(self):
  self.assertEqual(subprocess.run(['ffmpeg','-version'],stdout=subprocess.DEVNULL).returncode,0)
if __name__=='__main__': unittest.main()
