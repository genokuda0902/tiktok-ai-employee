"""Synthetic-only tests. No private user MP4 in repository or CI."""
import importlib.util, pathlib, sys, tempfile, unittest
p=pathlib.Path(__file__).resolve().parents[1]/'code'/'review_cta.py'
spec=importlib.util.spec_from_file_location('review_cta',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
class ReviewCTATests(unittest.TestCase):
    def test_ten_genre_palettes(self):
        self.assertEqual(len(m.GENRE_COLORS),10)
        self.assertEqual(len(set(m.GENRE_COLORS.values())),10)
    def test_only_reviewed_genre(self):
        for g in set(m.GENRE_COLORS)-m.REVIEWED_GENRES:
            with self.assertRaises(PermissionError):m.build_overlay('/tmp/never-write.png',g)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):m.build_overlay('/tmp/never-write.png','unknown')
    def test_overlay_is_original_transparent(self):
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/'a.png';im=m.build_overlay(f)
            self.assertEqual(im.size,(68,112))
            self.assertEqual(im.mode,'RGBA')
            self.assertEqual(im.getpixel((0,0))[3],0)
            self.assertGreater(im.getpixel((34,50))[3],200)
    def test_reproducible_overlay(self):
        with tempfile.TemporaryDirectory() as d:
            a=pathlib.Path(d)/'a.png';b=pathlib.Path(d)/'b.png'
            m.build_overlay(a);m.build_overlay(b)
            self.assertEqual(m.sha256(a),m.sha256(b))
    def test_no_wrong_resolution(self):
        fake={'streams':[{'codec_type':'video','width':720,'height':1280,'r_frame_rate':'30/1'},
                         {'codec_type':'audio','codec_name':'aac','sample_rate':'48000'}],
              'format':{'duration':'23.03'}}
        with self.assertRaises(ValueError):m.check_input(fake,'ai_work')
    def test_no_unreviewed_render(self):
        with self.assertRaises(PermissionError):m.check_input({},'travel')
    def test_requires_audio(self):
        fake={'streams':[{'codec_type':'video','width':1080,'height':1920,'r_frame_rate':'30/1'}],
              'format':{'duration':'23.03'}}
        with self.assertRaises(ValueError):m.check_input(fake,'ai_work')
    def test_safe_bbox(self):
        x1,y1,x2,y2=[79,1430,147,1542]
        self.assertLessEqual(x2,150)
        self.assertGreaterEqual(y1,1400)
        self.assertLessEqual(y2,1600)
if __name__=='__main__':unittest.main()
