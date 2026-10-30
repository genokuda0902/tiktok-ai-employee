import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from clean_hook import draw_slide,GENRES,W,H,PANEL_TOP,PANEL_BOTTOM
class TestCleanHook(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES: self.assertEqual(draw_slide(g).size,(W,H))
    def test_no_caption_overlap(self):
        im=draw_slide('ai_work')
        self.assertEqual(im.getpixel((500,1400))[3],0)
        self.assertEqual(im.getpixel((500,100))[3],0)
        self.assertEqual(im.getpixel((500,500))[3],255)
    def test_safety_content(self):
        s=(Path(__file__).resolve().parents[1]/'code'/'clean_hook.py').read_text()
        for bad in ('requests.post','tiktok.upload','auto_post','subprocess.run(["curl"'):
            self.assertNotIn(bad,s)
    def test_fail_closed_genre(self):
        with self.assertRaises(ValueError):draw_slide('unapproved_genre')
    def test_palette_unique(self):
        self.assertEqual(len(set(GENRES.values())),10)
if __name__=='__main__':unittest.main()
