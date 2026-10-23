import copy,json,unittest
from pathlib import Path
from protected_region_restore import validate,GENRES
C=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf8'))
class TestProtectedRegion(unittest.TestCase):
    def test_valid(self):self.assertTrue(validate(C))
    def test_ten_genres(self):
        for g in GENRES:
            c=copy.deepcopy(C);c['genre']=g;self.assertTrue(validate(c))
    def test_no_unapproved_publication(self):
        for field in ('publication_approved','rights_reviewed'):
            c=copy.deepcopy(C);c[field]=True
            with self.assertRaises(ValueError):validate(c)
    def test_no_unknown_genre(self):
        c=copy.deepcopy(C);c['genre']='unknown'
        with self.assertRaises(ValueError):validate(c)
    def test_bounds(self):
        for region in ([0,1300,1200,240],[-2,1300,1080,240],[0,1301,1080,240],[0,1300,1080,0]):
            c=copy.deepcopy(C);c['restore_region']=region
            with self.assertRaises(ValueError):validate(c)
    def test_protects_entire_cta(self):
        c=copy.deepcopy(C);c['restore_region']=[0,1300,500,240]
        with self.assertRaises(ValueError):validate(c)
    def test_time(self):
        for start,end in ((22,21),(0,70),(23.8,23.843)):
            c=copy.deepcopy(C);c['start_seconds']=start;c['end_seconds']=end
            with self.assertRaises(ValueError):validate(c)
    def test_clean_reference_required(self):
        c=copy.deepcopy(C);c['clean_reference_review_only']=False
        with self.assertRaises(ValueError):validate(c)
    def test_resolution(self):
        c=copy.deepcopy(C);c['canvas']=[720,1280]
        with self.assertRaises(ValueError):validate(c)
    def test_region_does_not_cover_top_headline(self):
        x,y,w,h=C['restore_region'];self.assertGreater(y,1000)
    def test_private_assets_never_bundled(self):
        self.assertNotIn('IMG_5805',str(C));self.assertNotIn('AI_Jitan_v33_REAL_SPREADSHEET',str(C))
if __name__=='__main__':unittest.main()
