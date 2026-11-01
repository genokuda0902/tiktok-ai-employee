import hashlib, json, subprocess, tempfile, unittest
from pathlib import Path
from formula_audit import GENRES, POLICY, validate, make_overlay, render

def fixture():
    return {'policy':POLICY,'asset_approval':'private_review_only','source_sha256':'abc','genre':'ai',
    'sheet':{'columns':{'B':[12,16,18],'C':[8,9,12]},'selected_cell':'C5','visible_formula':'=SUM(C2:C4)','visible_total':29,'other_total':46,'incorrect_overlay':'=SUM(B2:B4)'},
    'patch':{'start_frame':15,'end_frame':22,'bbox':[77,210,550,269],'text_origin':[82,215]}}

class FormulaAuditTest(unittest.TestCase):
    def test_ten_genres(self):
        for genre in GENRES:
            m=fixture();m['genre']=genre
            self.assertEqual(validate(m,'abc',60),(15,22))
    def test_wrong_column(self):
        m=fixture();m['sheet']['visible_formula']='=SUM(B2:B4)'
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_wrong_total(self):
        m=fixture();m['sheet']['visible_total']=46
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_wrong_other_total(self):
        m=fixture();m['sheet']['other_total']=29
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_wrong_row(self):
        m=fixture();m['sheet']['selected_cell']='C4'
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_mismatched_source(self):
        with self.assertRaises(ValueError):validate(fixture(),'other',60)
    def test_no_correction_needed(self):
        m=fixture();m['sheet']['incorrect_overlay']=m['sheet']['visible_formula']
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_unsafe_patch(self):
        m=fixture();m['patch']['bbox']=[77,1400,550,1460]
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_unknown_genre(self):
        m=fixture();m['genre']='unknown'
        with self.assertRaises(ValueError):validate(m,'abc',60)
    def test_overlay_confined(self):
        im=make_overlay(fixture(),540,960)
        self.assertEqual(im.getpixel((10,850))[3],0)
        self.assertEqual(im.getpixel((100,110))[3],255)
    def test_synthetic_av(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);src=d/'src.mp4';dst=d/'out.mp4';manifest=d/'manifest.json';report=d/'report.json'
            subprocess.run(['ffmpeg','-hide_banner','-v','error','-f','lavfi','-i','color=c=navy:s=540x960:r=30:d=1.5','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.5','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)],check=True)
            m=fixture();m['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
            manifest.write_text(json.dumps(m))
            qa=render(src,dst,manifest,report)
            self.assertEqual(qa['full_av_decode'],'PASS')
            self.assertTrue(qa['audio_adts_unchanged'])
            self.assertEqual(qa['frames'],45)
if __name__=='__main__':unittest.main()
