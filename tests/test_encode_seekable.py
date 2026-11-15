import unittest
from pathlib import Path
from unittest.mock import patch
from tools.encode_seekable import encode

class TestEncoder(unittest.TestCase):
    def test_output_parent_created(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/'nested'/'a.mp4'
            with patch('tools.encode_seekable.subprocess.run') as run:
                self.assertEqual(encode(Path('in.mp4'),dest),dest)
                self.assertTrue(dest.parent.is_dir())
                cmd=run.call_args.args[0]
                self.assertIn('+faststart',cmd)
                self.assertIn('expr:gte(t,n_forced*2)',cmd)
                self.assertIn('copy',cmd)

if __name__=='__main__': unittest.main()
