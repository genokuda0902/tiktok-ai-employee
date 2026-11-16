import unittest
from render import command

class ExportTests(unittest.TestCase):
    def test_vertical_hd(self):
        cmd=command('in.mp4','out.mp4')
        self.assertIn('scale=1080:1920:flags=lanczos',cmd[cmd.index('-vf')+1])
    def test_safe_output(self):
        cmd=command('in.mp4','out.mp4')
        self.assertIn('+faststart',cmd)
        self.assertIn('-an',cmd)
    def test_no_publish(self):
        cmd=command('in.mp4','out.mp4')
        self.assertNotIn('upload', ' '.join(cmd))
if __name__=='__main__': unittest.main()
