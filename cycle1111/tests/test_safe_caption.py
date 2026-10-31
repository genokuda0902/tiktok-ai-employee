import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from safe_caption import GENRES, SCENES, CAPTION_RIGHT, CAPTION_BOTTOM, make_ass, command

class TestSafeCaption(unittest.TestCase):
    def test_genres(self):
        for genre in GENRES:
            with self.subTest(genre=genre), tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp)/'test.ass';make_ass(out,genre=genre)
                self.assertEqual(out.read_text().count('Dialogue: '),16)
    def test_eight_scenes(self):
        self.assertEqual(len(SCENES),8)
        self.assertEqual(SCENES[0][0],0)
        self.assertEqual(SCENES[-1][1],22.5)
    def test_safe_zones(self):
        self.assertLessEqual(CAPTION_RIGHT,900)
        self.assertLessEqual(CAPTION_BOTTOM,1650)
    def test_bad_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_ass(Path(tmp)/'bad.ass',[(0,1,'x','y')])
    def test_audio_is_copied(self):
        cmd=command('in.mp4','out.mp4','x.ass')
        self.assertEqual(cmd[cmd.index('-c:a')+1],'copy')
    def test_no_network(self):
        code=(Path(__file__).resolve().parents[1]/'code'/'safe_caption.py').read_text()
        self.assertNotIn('requests.post(',code)
if __name__=='__main__': unittest.main()
