import json
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from hook_layout import GENRES, CARDS, CAPTION, SAFE, check_config, fit_font, make_background, make_frame, card_motion_dx

CFG=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf8'))
class TestHookLayout(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_contract(self): self.assertTrue(check_config(CFG))
    def test_animation_stays_in_safe(self):
        for t in (0.0,0.1,0.25,0.52,1.2,3.1):
            for i,b in enumerate(CARDS):
                dx=card_motion_dx(i,t)
                self.assertGreaterEqual(b[0]+dx,SAFE[0])
                self.assertLessEqual(b[2]+dx,SAFE[2])
    def test_full_text_fits(self):
        d=ImageDraw.Draw(Image.new('RGB',(1000,1000)))
        for txt in (CFG['before_label'],CFG['after_label']):
            f=fit_font(d,txt,344,36)
            self.assertLessEqual(d.textbbox((0,0),txt,font=f)[2],344)
    def test_unknown_genre_rejected(self):
        c=dict(CFG);c['genre']='unknown'
        with self.assertRaises(ValueError):check_config(c)
    def test_no_publication(self):
        c=dict(CFG);c['publication_approved']=True
        with self.assertRaises(ValueError):check_config(c)
    def test_rights_gate(self):
        c=dict(CFG);c['rights_reviewed']=True
        with self.assertRaises(ValueError):check_config(c)
    def test_caption_below_cards(self):self.assertGreater(CAPTION[1],max(b[3] for b in CARDS))
    def test_ui_safe_margin(self):
        self.assertTrue(all(SAFE[0]<=b[0]<b[2]<=SAFE[2] for b in CARDS))
        self.assertLessEqual(CAPTION[2],SAFE[2])
    def test_render_determinism(self):
        a=Image.new('RGB',(344,286),(60,80,95));b=Image.new('RGB',(337,277),(95,140,160))
        bg=make_background()
        one=make_frame(1.0,bg,(a,b),CFG)
        two=make_frame(1.0,bg,(a,b),CFG)
        self.assertEqual(one.tobytes(),two.tobytes())
        self.assertEqual(one.size,(1080,1920))
    def test_nonempty_hook_regions(self):
        a=Image.new('RGB',(344,286),(60,80,95));b=Image.new('RGB',(337,277),(95,140,160))
        im=make_frame(1.0,make_background(),(a,b),CFG)
        self.assertNotEqual(im.getpixel((100,1100)),im.getpixel((100,1500)))
if __name__=='__main__':unittest.main()
