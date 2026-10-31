import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from jp_chrome import GENRE_LABELS, GLOBAL_PATCHES, LATER_PATCHES, SCENE1_PATCHES, render_layers, build_ffmpeg_cmd, W, H

class TestJapaneseChrome(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_LABELS), 10)
        self.assertTrue(all(v for v in GENRE_LABELS.values()))
    def test_bounds(self):
        for rect, color in GLOBAL_PATCHES + SCENE1_PATCHES + LATER_PATCHES:
            x0,y0,x1,y1=rect
            self.assertTrue(0<=x0<x1<W and 0<=y0<y1<H)
            self.assertEqual(color[3],255)
    def test_layers_and_alpha(self):
        with tempfile.TemporaryDirectory() as d:
            paths=render_layers(d)
            self.assertEqual(len(paths),3)
            for p in paths:
                with Image.open(p) as im:
                    self.assertEqual(im.size,(W,H))
                    self.assertEqual(im.mode,'RGBA')
                    self.assertEqual(im.getpixel((1079,1919))[3],0)
            with Image.open(paths[0]) as im:
                self.assertEqual(im.getpixel((100,100))[3],255)
                self.assertEqual(im.getpixel((640,90))[3],0) # preserve reactive bars
                self.assertEqual(im.getpixel((950,90))[3],0) # preserve step number
    def test_all_genres_render(self):
        with tempfile.TemporaryDirectory() as d:
            for genre in GENRE_LABELS:
                paths=render_layers(Path(d)/genre,genre)
                self.assertTrue(all(p.stat().st_size>1000 for p in paths))
    def test_audio_stream_copy(self):
        paths=[Path('/tmp/a.png'),Path('/tmp/b.png'),Path('/tmp/c.png')]
        cmd=build_ffmpeg_cmd('in.mp4','out.mp4',paths,22.5,94/30)
        self.assertEqual(cmd[cmd.index('-c:a')+1],'copy')
        self.assertEqual(cmd[cmd.index('-map_chapters')+1],'0')
        self.assertIn("lt(t,3.133333)",cmd[cmd.index('-filter_complex')+1])
    def test_reject_bad_duration(self):
        with self.assertRaises(ValueError):
            build_ffmpeg_cmd('in.mp4','out.mp4',[Path('a')]*3,3,3)
    def test_unknown_genre(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): render_layers(d,'not_a_genre')

if __name__=='__main__': unittest.main()
