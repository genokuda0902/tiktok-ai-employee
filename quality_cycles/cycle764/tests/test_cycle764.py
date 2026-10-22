import unittest,sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from make_slides import create,get_genres
from render import render
class TestCycle764(unittest.TestCase):
    def test_genres_10(self):self.assertEqual(len(get_genres()),10)
    def test_each_genre_image(self):
        for g in get_genres():self.assertEqual(create(1,g['name']).size,(1080,1920))
    def test_distinct_stages(self):
        imgs=[create(i).resize((108,192)).tobytes() for i in (1,2,3)]
        self.assertEqual(len(set(imgs)),3)
    def test_invalid_stage(self):
        with self.assertRaises(ValueError):create(4)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):create(1,'INVALID')
    def test_invalid_step_count(self):
        with self.assertRaises(ValueError):create(1,steps=[('1','2','3')])
    def test_invalid_windows(self):
        with self.assertRaises(ValueError):render('x.mp4',['a.png'],'o.mp4',[(3,2)])
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):render('x.mp4',['a.png','b.png'],'o.mp4',[(1,2),(2.5,3)])
    def test_mismatch_rejected(self):
        with self.assertRaises(ValueError):render('x.mp4',['a.png'],'o.mp4',[(1,2),(2,3)])
    def test_16_japanese_cues(self):
        import re
        s=(ROOT/'config/phrase_cues.srt').read_text(encoding='utf8')
        self.assertEqual(len(re.findall(r'(?m)^\d+\s*$',s)),16)
        self.assertIn('入力、処理、',s);self.assertIn('出力。',s)
if __name__=='__main__':unittest.main()
