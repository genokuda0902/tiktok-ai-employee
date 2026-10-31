import importlib.util, pathlib, unittest
from PIL import Image
P=pathlib.Path(__file__).resolve().parents[1]/'source'/'proof_first_teaser.py'
spec=importlib.util.spec_from_file_location('teaser1042',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestProofFirstTeaser(unittest.TestCase):
    def test_10_genre_palettes(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(set(m.GENRES),set(m.PALETTES))
        for g in m.GENRES:
            self.assertEqual(len(m.PALETTES[g]),2)
            self.assertEqual(len(m.rgb(m.PALETTES[g][0])),3)
    def test_three_cuts_exact(self):
        self.assertEqual([m.shot_index(f) for f in (45,58,59,72,73,86)],[0,0,1,1,2,2])
        self.assertEqual(m.END_FRAME-m.START_FRAME,42)
        with self.assertRaises(ValueError):m.shot_index(87)
    def test_safe_height_and_original_art(self):
        still=Image.new('RGB',(1080,1920),'#113355')
        for g in m.GENRES:
            for f in (45,59,73):
                im=m.teaser_frame(f,still,g)
                self.assertEqual(im.size,(1080,1280))
                self.assertEqual(im.getpixel((0,0))[3],255)
    def test_fail_closed_unknown_and_unapproved(self):
        with self.assertRaises(ValueError):m.validate('missing.mp4',m.SOURCE_SHA,'ai_work',False)
        with self.assertRaises(ValueError):m.validate('missing.mp4',m.SOURCE_SHA,'beauty',True)
        with self.assertRaises(ValueError):m.validate('missing.mp4',m.SOURCE_SHA,'unknown',True)
    def test_proof_frames_distinct_and_later_than_intro(self):
        f=[x[0] for x in m.SHOT_SPECS]
        self.assertEqual(len(set(f)),3)
        self.assertTrue(all(x>m.END_FRAME for x in f))
    def test_no_network_or_publication(self):
        code=P.read_text()
        self.assertNotIn('requests.',code)
        self.assertNotIn('upload',code.lower().split('def render(')[-1])
        self.assertIn('PUBLICATION_NOT_APPROVED',code)

if __name__=='__main__':unittest.main()
