import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image
spec=importlib.util.spec_from_file_location('proof',Path(__file__).parents[1]/'source'/'arithmetic_proof.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class ProofTests(unittest.TestCase):
    def test_source_math(self): self.assertTrue(mod.verify_ledger())
    def test_wrong_sum_rejected(self):
        with self.assertRaises(ValueError):mod.verify_ledger(totals=(45,29))
    def test_negative_rejected(self):
        with self.assertRaises(ValueError):mod.verify_ledger(a=(-1,16,18),totals=(33,29))
    def test_boolean_rejected(self):
        with self.assertRaises(ValueError):mod.verify_ledger(a=(True,16,18),totals=(35,29))
    def test_unproven_data_rejected(self):
        with self.assertRaises(ValueError):mod.verify_ledger(fictional=False)
    def test_ten_genre_list(self): self.assertEqual(len(mod.GENRES),10)
    def test_other_genres_fail_closed(self):
        for g in mod.GENRES[1:]:
            with self.assertRaises(ValueError):mod.check_policy(g,True,'0'*64)
    def test_review_gate(self):
        with self.assertRaises(ValueError):mod.check_policy('ai_work',False,'0'*64)
    def test_sha_gate(self):
        with self.assertRaises(ValueError):mod.check_policy('ai_work',True,'bad')
    def test_card_safe_area(self):
        x,y,w,h=mod.BOX
        self.assertGreaterEqual(x,50)
        self.assertLess(y+h,1280)
        self.assertLessEqual(x+w,1080)
    def test_card_is_transparent_outside_content(self):
        with tempfile.TemporaryDirectory() as d:
            path=mod.create_card(Path(d)/'card.png')
            im=Image.open(path)
            self.assertEqual(im.size,mod.BOX[2:])
            self.assertEqual(im.getpixel((0,0))[3],0)
            self.assertGreater(im.getpixel((100,100))[3],200)
    def test_window_validation(self):
        with self.assertRaises(ValueError):mod.build_command('a','b','c',(0.0,.2))
    def test_audio_subtitle_stream_copy(self):
        cmd=mod.build_command('a','b','c')
        self.assertIn('-c:a',cmd);self.assertEqual(cmd[cmd.index('-c:a')+1],'copy')
        self.assertEqual(cmd[cmd.index('-c:s')+1],'copy')
    def test_caption_safe_overlay(self):
        cmd=mod.build_command('a','b','c')
        self.assertIn('overlay=x=75:y=972',cmd[cmd.index('-filter_complex')+1])
if __name__=='__main__':unittest.main()
