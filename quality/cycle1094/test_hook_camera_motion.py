import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image,ImageChops
from quality.cycle1094 import hook_camera_motion as g
M=json.loads((Path(__file__).parent/'manifest.json').read_text())

class HookCameraMotionTests(unittest.TestCase):
    def test_ten_genre_presets_and_safe_region(self):
        for genre in g.PALETTES:
            m=dict(M,genre=genre)
            self.assertTrue(g.validate(m))
            self.assertLess(g.ROI[1]+g.ROI[3],g.CAPTION_START_Y)

    def test_smooth_push_in(self):
        zs=[g.camera_params(i,45,M)[0] for i in range(45)]
        self.assertAlmostEqual(zs[0],1.0)
        self.assertAlmostEqual(zs[-1],1.12)
        self.assertTrue(all(a<=b for a,b in zip(zs,zs[1:])))
        self.assertLess(max(b-a for a,b in zip(zs,zs[1:])),.005)

    def test_no_visual_change_at_initial_frame(self):
        im=Image.new('RGB',g.ROI[2:],'#154578')
        self.assertIsNone(ImageChops.difference(im,g.motion_frame(im,0,45,M)).getbbox())

    def test_motion_changes_middle_without_roi_edge_seam(self):
        im=Image.new('RGB',g.ROI[2:])
        from PIL import ImageDraw
        d=ImageDraw.Draw(im)
        for i in range(0,g.ROI[2],17):d.line((i,0,i,g.ROI[3]),fill='#ffffff',width=2)
        transformed=g.motion_frame(im,33,45,M)
        self.assertIsNotNone(ImageChops.difference(im,transformed).getbbox())
        for pt in ((0,0),(0,375),(899,749),(450,0),(450,749)):
            self.assertEqual(im.getpixel(pt),transformed.getpixel(pt))

    def test_review_only_and_privacy_fail_closed(self):
        for k,v in [('synthetic_scenario',False),('review_only',False),
                    ('rights_status','approved'),('contains_private_data',True),
                    ('zoom_max',1.5),('focus_x',0.2),('genre','unknown')]:
            with self.subTest(k=k):
                with self.assertRaises(ValueError):g.validate(dict(M,**{k:v}))

    def test_source_sha_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'source';src.write_bytes(b'not-a-video')
            with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
                g.render(src,Path(tmp)/'out.mp4','0'*64,M)

    def test_invalid_frame(self):
        for i in (-1,45,100):
            with self.assertRaises(ValueError):g.camera_params(i,45,M)

if __name__=='__main__':unittest.main()
