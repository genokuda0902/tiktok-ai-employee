import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cta_voice_guard as c

M={'genre':'ai_work','synthetic_scenario':True,'review_only':True,
   'rights_status':'unverified','contains_private_data':False,
   'cta_text':'次は1つ試す','start_seconds':21.966667}

class ReviewOnlyTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(c.PALETTES),10)
        for genre in c.PALETTES:
            m={**M,'genre':genre};self.assertTrue(c.validate_manifest(m))
            self.assertEqual(c.make_cta_frame(18,30,genre).size,(c.CTA_W,c.CTA_H))
    def test_fail_closed_rights(self):
        for key,value in [('review_only',False),('synthetic_scenario',False),
                          ('rights_status','approved'),('contains_private_data',True)]:
            with self.assertRaises(ValueError):c.validate_manifest({**M,key:value})
    def test_reject_extra_fields(self):
        with self.assertRaises(ValueError):c.validate_manifest({**M,'autopost':True})
    def test_reject_unreviewed_cta(self):
        with self.assertRaises(ValueError):c.validate_manifest({**M,'cta_text':'フォローで100倍時短'})
    def test_reject_outside_final_scene(self):
        with self.assertRaises(ValueError):c.validate_manifest({**M,'start_seconds':17.0})
    def test_protected_caption_area(self):
        self.assertLess(c.CTA_Y+c.CTA_H,c.CAPTION_START_Y)
    def test_fade_is_monotone(self):
        for x in (0,0.2,0.5,1):self.assertGreaterEqual(c.ease(x),0)
        self.assertLess(c.ease(0.1),c.ease(0.5))
    def test_alpha_ramp(self):
        a=c.make_cta_frame(0,30,'ai_work').getchannel('A')
        b=c.make_cta_frame(10,30,'ai_work').getchannel('A')
        self.assertLess(sum(a.tobytes()),sum(b.tobytes()))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):c.validate_manifest({**M,'genre':'illegal'})
    def test_pin_mismatch_before_render(self):
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/'source.mp4';source.write_bytes(b'fictional synthetic bytes')
            with self.assertRaises(ValueError):c.render(source,Path(td)/'out.mp4','0'*64,M)

if __name__=='__main__':unittest.main()
