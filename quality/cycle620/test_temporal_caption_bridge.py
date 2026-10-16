import unittest
import numpy as np
from temporal_caption_bridge import GENRES, BridgeSpec, blend_whole, bridge_frame, smoothstep

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.a=np.zeros((12,32,3),dtype=np.uint8)
        self.b=np.full_like(self.a,200)
        self.spec=BridgeSpec()
    def test_real_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertIn('商品比較・暮らし',GENRES.values())
        self.assertIn('営業・ビジネス',GENRES.values())
        for genre in GENRES: BridgeSpec(genre=genre).validate()
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): BridgeSpec(genre='miniature').validate()
    def test_publication_fail_closed(self):
        with self.assertRaises(ValueError): BridgeSpec(publication_status='APPROVED').validate()
    def test_frame_range(self):
        for n in (17,46,26):
            with self.assertRaises(ValueError):BridgeSpec(frames=n).validate()
    def test_frame_boundaries(self):
        with self.assertRaises(ValueError):bridge_frame(self.a,self.b,27,self.spec)
    def test_endpoints(self):
        self.assertTrue(np.array_equal(bridge_frame(self.a,self.b,0,self.spec),self.a))
        self.assertTrue(np.array_equal(bridge_frame(self.a,self.b,26,self.spec),self.b))
    def test_center_is_caption_free_slate(self):
        x=bridge_frame(self.a,self.b,13,self.spec)
        self.assertTrue(np.all(x==np.asarray(self.spec.slate_rgb,dtype=np.uint8)))
    def test_no_spatial_wipe_or_split(self):
        a=np.zeros((10,80,3),dtype=np.uint8)
        b=np.full_like(a,255)
        x=blend_whole(a,b,.4)
        self.assertEqual(int(x.max()),int(x.min()))
        self.assertTrue(np.all(x==102))
    def test_blend_endpoints(self):
        self.assertTrue(np.array_equal(blend_whole(self.a,self.b,0),self.a))
        self.assertTrue(np.array_equal(blend_whole(self.a,self.b,1),self.b))
    def test_bad_opacity(self):
        with self.assertRaises(ValueError):blend_whole(self.a,self.b,1.01)
    def test_bad_dtype(self):
        with self.assertRaises(ValueError):blend_whole(self.a,self.b.astype('float32'),.5)
    def test_smoothstep(self):
        self.assertEqual(smoothstep(0),0)
        self.assertEqual(smoothstep(1),1)
        self.assertAlmostEqual(smoothstep(.5),.5)
        with self.assertRaises(ValueError):smoothstep(-.01)
    def test_mid_fade_uniformity(self):
        for i in (2,7,18,24):
            x=bridge_frame(self.a,self.b,i,self.spec)
            self.assertTrue(np.all(x==x[0,0,:]))
    def test_invalid_slate(self):
        with self.assertRaises(ValueError):BridgeSpec(slate_rgb=(300,0,0)).validate()

if __name__=='__main__':unittest.main()
