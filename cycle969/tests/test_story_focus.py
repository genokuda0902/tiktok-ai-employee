import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('story_focus',Path(__file__).resolve().parents[1]/'code/story_focus.py')
sf=importlib.util.module_from_spec(spec);spec.loader.exec_module(sf)

class FocusTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(sf.GENRE_COLORS),10)
    def test_other_genres_fail_closed(self):
        for g in sf.GENRE_COLORS.keys()-sf.REVIEWED_GENRES:
            with self.assertRaises(PermissionError): sf.overlay_frame(35,g)
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): sf.validate({},'unknown')
    def test_order(self):
        self.assertEqual(sf.alpha_at(9)[0],'sorting')
        self.assertEqual(sf.alpha_at(20)[0],'mail')
        self.assertEqual(sf.alpha_at(38)[0],'weekly')
    def test_ends_before_scene2(self): self.assertIsNone(sf.alpha_at(80)[0])
    def test_early_frame_empty(self): self.assertIsNone(sf.overlay_frame(0).getbbox())
    def test_visual_nonempty(self): self.assertIsNotNone(sf.overlay_frame(39).getbbox())
    def test_safe_region(self):
        self.assertLessEqual(sf.REGION[3],975)
        self.assertLess(sf.REGION[3],1180)
        for box in sf.CARDS.values(): self.assertLess(box[3],sf.REGION[3])
    def test_card_continuity(self): self.assertEqual(sf.CARDS['weekly'][0],70)
    def test_frame_size(self): self.assertEqual(sf.overlay_frame(38).size,(900,475))
    def test_overlay_not_full_screen(self):
        im=sf.overlay_frame(38)
        self.assertLess(sum(1 for p in im.getchannel('A').getdata() if p),(im.width*im.height)//5)
    def test_media_contract(self):
        info={'streams':[{'codec_type':'video','codec_name':'h264','width':1080,'height':1920,'r_frame_rate':'30/1'},
                         {'codec_type':'audio','codec_name':'aac','sample_rate':'48000'}],
              'format':{'duration':'23.0333'}}
        self.assertAlmostEqual(sf.validate(info,'ai_work'),23.0333)
        info['streams'][0]['width']=720
        with self.assertRaises(ValueError): sf.validate(info,'ai_work')

if __name__=='__main__':unittest.main()
