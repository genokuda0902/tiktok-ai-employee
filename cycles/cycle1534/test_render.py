import json, subprocess, tempfile, unittest
from pathlib import Path
class ProgressOverlayTests(unittest.TestCase):
    def test_script_compiles(self):
        compile(Path(__file__).with_name('render.py').read_text(), 'render.py','exec')
    def test_ffmpeg_available(self):
        subprocess.run(['ffmpeg','-version'],stdout=subprocess.DEVNULL,check=True)
    def test_source_is_required(self):
        p=subprocess.run(['python',str(Path(__file__).with_name('render.py')), '/missing-input.mp4'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('FileNotFoundError',p.stderr)
if __name__=='__main__': unittest.main()
