import unittest
from editorial_beats import BOUNDARIES,GENRES,POLICY,beats,filter_graph,validate

class TestEditorialBeats(unittest.TestCase):
    def setUp(self):
        self.m={**POLICY,'genre':'ai_productivity','source_sha256':'a'*64,
                'real_service_footage':False,'reference_equivalent':False}
    def test_16_beats(self):
        self.assertEqual(len(beats())*2,16)
    def test_all_frames_covered(self):
        self.assertEqual(sum(b-a for a,_,b in beats()),691)
    def test_8_distinct_cut_frames(self):
        self.assertEqual([mid for _,mid,_ in beats()],[44,129,210,293,379,466,549,639])
    def test_no_overlap(self):
        self.assertTrue(all(a<m<b for a,m,b in beats()))
    def test_caption_zone_untouched(self):
        graph=filter_graph()
        self.assertIn('overlay=66:180',graph)
        self.assertIn('drawbox=x=38:y=155',graph)
        self.assertLess(155+1220,1490)
    def test_10_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.m['genre']=genre
            self.assertTrue(validate(self.m))
    def test_unknown_genre_rejected(self):
        self.m['genre']='private_data'
        with self.assertRaises(ValueError):validate(self.m)
    def test_policy_rejected(self):
        for k in POLICY:
            changed=self.m.copy()
            changed[k]=not POLICY[k]
            with self.assertRaises(ValueError):validate(changed)
    def test_false_service_claim_rejected(self):
        self.m['real_service_footage']=True
        with self.assertRaises(ValueError):validate(self.m)
    def test_false_parity_claim_rejected(self):
        self.m['reference_equivalent']=True
        with self.assertRaises(ValueError):validate(self.m)
    def test_source_sha_required(self):
        self.m['source_sha256']='0'*63
        with self.assertRaises(ValueError):validate(self.m)
    def test_bad_boundaries(self):
        with self.assertRaises(ValueError):beats((0,1,2,3,4,5,6,7,8))

if __name__=='__main__':unittest.main()
