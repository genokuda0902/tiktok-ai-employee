import unittest
from PIL import Image, ImageChops
from hook_upgrade import GENRE_HOOKS, W,H,HOOK_FRAMES,stage,validate,composite_hook

class HookUpgradeTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRE_HOOKS),10)
        for genre in GENRE_HOOKS: self.assertEqual(len(validate(genre)),5)
    def test_fail_closed_rights(self):
        with self.assertRaises(ValueError):validate(rights='APPROVED')
    def test_fail_closed_publication(self):
        with self.assertRaises(ValueError):validate(publication='APPROVED')
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate('unknown')
    def test_early_hook(self):
        self.assertEqual(stage(0),'question')
        self.assertEqual(stage(16),'question')
        self.assertEqual(stage(17),'proof')
        self.assertEqual(stage(38),'result')
    def test_bad_frame(self):
        for x in (-1,66,1.2):
            with self.assertRaises(ValueError):stage(x)
    def test_canvas_size_and_kinetic_change(self):
        bg=Image.new('RGB',(W,H),(10,30,50))
        a=composite_hook(bg,0); b=composite_hook(bg,42)
        self.assertEqual(a.size,(W,H))
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
    def test_no_fabricated_speed_claim(self):
        for fields in GENRE_HOOKS.values():
            self.assertFalse(any('10倍' in s or '秒で完了' in s for s in fields))
    def test_inherited_rights_unapproved(self):
        self.assertEqual(validate('ai_work')[-1],'720')

if __name__=='__main__': unittest.main()
