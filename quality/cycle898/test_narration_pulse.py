import tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from narration_pulse import *

class TestPulse(unittest.TestCase):
    def good(self,genre='ai_productivity'):
        return {**POLICY,'genre':genre,'source_sha256':'a'*64,
                'real_service_footage':False,'reference_equivalent':False}
    def test_genres(self):
        for g in GENRES:self.assertTrue(validate_manifest(self.good(g)))
    def test_bad_genre(self):
        with self.assertRaises(ValueError):validate_manifest(self.good('unknown'))
    def test_publication_denied(self):
        m=self.good();m['publication_approved']=True
        with self.assertRaises(ValueError):validate_manifest(m)
    def test_private_upload_denied(self):
        m=self.good();m['external_upload']=True
        with self.assertRaises(ValueError):validate_manifest(m)
    def test_bad_hash(self):
        m=self.good();m['source_sha256']='not-a-hash'
        with self.assertRaises(ValueError):validate_manifest(m)
    def test_reference_claim_denied(self):
        m=self.good();m['reference_equivalent']=True
        with self.assertRaises(ValueError):validate_manifest(m)
    def test_audio_length(self):
        with self.assertRaises(ValueError):smooth_envelope([0]*10)
    def test_invalid_audio(self):
        with self.assertRaises(ValueError):smooth_envelope([float('nan')]*FRAMES)
    def test_smoothing(self):
        x=smooth_envelope([0]*40+[0.1]*80+[0]*(FRAMES-120))
        self.assertTrue(0<x[40]<x[50]<=1)
        self.assertTrue(x[130]<x[119])
    def test_bars(self):
        x=smooth_envelope([0.01]*FRAMES)
        self.assertEqual(len(bars(x,50)),5)
        self.assertTrue(all(4<=n<=32 for n in bars(x,50)))
    def test_png(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.png';write_png(p,[4,10,20,30,5])
            self.assertEqual(p.read_bytes()[:8],b'\x89PNG\r\n\x1a\n')
            self.assertGreater(p.stat().st_size,100)
    def test_caption_safe(self):
        self.assertLess(Y+HEIGHT,1490)
    def test_frame_count(self):
        self.assertEqual(FRAMES,691)
    def test_unknown_claim(self):
        m=self.good();m['real_service_footage']=True
        with self.assertRaises(ValueError):validate_manifest(m)

if __name__=='__main__':unittest.main()
