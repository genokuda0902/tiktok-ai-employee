import copy,json,unittest
from pathlib import Path
from PIL import Image
from proof_magnifier import validate,stage,draw_patch,GENRES,POLICY,START,END,X,Y,W,H

SAMPLE=json.loads((Path(__file__).parent/'manifest_local.json').read_text(encoding='utf-8'))

class MagnifierTests(unittest.TestCase):
    def test_all_genres(self):
        for genre in GENRES:
            m=copy.deepcopy(SAMPLE);m['genre']=genre;self.assertTrue(validate(m))
    def test_unknown_genre_rejected(self):
        m=copy.deepcopy(SAMPLE);m['genre']='unknown'
        with self.assertRaises(ValueError):validate(m)
    def test_release_policy_fail_closed(self):
        for key,value in POLICY.items():
            m=copy.deepcopy(SAMPLE);m[key]=not value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(m)
    def test_missing_policy_rejected(self):
        m=copy.deepcopy(SAMPLE);m.pop('review_only')
        with self.assertRaises(ValueError):validate(m)
    def test_roi_out_of_bounds(self):
        for roi in [[0,0,1100,1600],[600,600,550,700],[0,500,20,600],[0.1,200,400,500]]:
            m=copy.deepcopy(SAMPLE);m['roi']=roi
            with self.subTest(roi=roi),self.assertRaises(ValueError):validate(m)
    def test_stage_boundaries(self):
        self.assertEqual([stage(x) for x in (0,25,26,51,52,77)],[0,0,1,1,2,2])
        for n in (-1,78,3.5,True):
            with self.assertRaises(ValueError):stage(n)
    def test_bad_stages(self):
        m=copy.deepcopy(SAMPLE);m['stages']=m['stages'][:2]
        with self.assertRaises(ValueError):validate(m)
    def test_unsafe_claims_and_pii(self):
        for value in ['https://example.com','person@example.com','12345678','2時間短縮','50%改善','<script>']:
            m=copy.deepcopy(SAMPLE);m['stages'][0]['label']=value
            with self.subTest(value=value),self.assertRaises(ValueError):validate(m)
    def test_text_overflow(self):
        m=copy.deepcopy(SAMPLE);m['stages'][0]['title']='長'*13
        with self.assertRaises(ValueError):validate(m)
    def test_sha_required(self):
        m=copy.deepcopy(SAMPLE);m['source_sha256']='notsha'
        with self.assertRaises(ValueError):validate(m)
    def test_render_3_distinct_states(self):
        crop=Image.new('RGB',(345,235),'white')
        imgs=[draw_patch(f,SAMPLE,crop) for f in (12,39,65)]
        self.assertTrue(all(im.size==(W,H) for im in imgs))
        self.assertEqual(len({im.tobytes() for im in imgs}),3)
    def test_caption_safe_area(self):
        self.assertLess(Y+H,1490)
        self.assertGreaterEqual(X,60)
        self.assertLessEqual(X+W,1020)
    def test_frame_range(self):
        self.assertEqual((START,END,END-START),(510,588,78))

if __name__=='__main__':unittest.main()
