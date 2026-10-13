"""Regression tests for cycle537 review-only clean CTA/loop."""
import json
import unittest
from pathlib import Path
from PIL import ImageChops
from clean_cta_loop import validate, cta_frame, GENRES, W, H, START, CTA_END, DURATION

C={"genre":"AI・仕事効率化","rights":"SYNTHETIC_OR_OWNER_APPROVED",
   "contains_private_data":False,"review_status":"HUMAN_REVIEW",
   "publication":"NOT_APPROVED","claims_real_results":False,
   "brand":"AI時短ラボ","cta":"保存して、あとで試そう",
   "step_1":"日本語で指示する","step_2":"合計を検算する","step_3":"グラフで確認する"}

class TestCleanCTA(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES: self.assertTrue(validate(dict(C,genre=g)))
    def test_reject_unknown_rights(self):
        with self.assertRaises(ValueError): validate(dict(C,rights='UNKNOWN'))
    def test_reject_private_data(self):
        with self.assertRaises(ValueError): validate(dict(C,contains_private_data=True))
    def test_reject_publication(self):
        with self.assertRaises(ValueError): validate(dict(C,publication='APPROVED'))
    def test_reject_claims(self):
        with self.assertRaises(ValueError): validate(dict(C,claims_real_results=True))
    def test_reject_bad_text(self):
        with self.assertRaises(ValueError): validate(dict(C,cta='A'*80))
    def test_reject_newline(self):
        with self.assertRaises(ValueError): validate(dict(C,step_1='A\nB'))
    def test_opaque_frame(self):
        im=cta_frame(.5,C)
        self.assertEqual(im.size,(W,H))
        self.assertEqual(im.mode,'RGB')
    def test_animation(self):
        self.assertIsNotNone(ImageChops.difference(cta_frame(0,C),cta_frame(.8,C)).getbbox())
    def test_bottom_safe(self):
        im=cta_frame(.7,C)
        self.assertEqual(im.getpixel((500,1740)),im.getpixel((501,1740)))
    def test_frame_count(self):
        self.assertEqual(round(START*30)+round((CTA_END-START)*30)+round((DURATION-CTA_END)*30),600)

if __name__=='__main__': unittest.main()
