import tempfile
import unittest
from pathlib import Path
from loop_reentry import GENRES, SUBS, validate_contract, make_srt, make_card, sha256, FONT

class TestLoopReentry(unittest.TestCase):
    def test_ten_genres_contract(self):
        for g in GENRES:self.assertTrue(validate_contract(g,SUBS))
    def test_timeline_complete(self):
        self.assertEqual(SUBS[0][0],0);self.assertEqual(SUBS[-1][1],20)
    def test_all_captions_at_least_one_second(self):
        self.assertTrue(all(b-a>=1 for a,b,_ in SUBS))
    def test_no_gap(self):
        with self.assertRaisesRegex(ValueError,'gap'):validate_contract('ai_productivity',SUBS[:5]+((12.1,16,'x'),)+SUBS[6:])
    def test_unknown_genre_rejected(self):
        with self.assertRaisesRegex(ValueError,'unknown'):validate_contract('unknown',SUBS)
    def test_empty_caption_rejected(self):
        with self.assertRaisesRegex(ValueError,'missing'):validate_contract('ai_productivity',((0,20,''),))
    def test_short_caption_rejected(self):
        with self.assertRaisesRegex(ValueError,'under'):validate_contract('ai_productivity',((0,0.5,'a'),(0.5,20,'b')))
    def test_loop_caption_matches_hook(self):
        self.assertEqual(SUBS[0][2],SUBS[-1][2])
    def test_srt_valid(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'captions.srt';make_srt(p);s=p.read_text()
            self.assertEqual(s.count('-->'),9)
            self.assertIn('00:00:19,000 --> 00:00:20,000',s)
    def test_card_geometry(self):
        if not Path(FONT).exists():self.skipTest('Noto Japanese font unavailable in runner')
        from PIL import Image
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'card.png';make_card(p)
            self.assertEqual(Image.open(p).size,(1080,1920))
    def test_sha(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x';p.write_bytes(b'abc')
            self.assertEqual(sha256(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
if __name__=='__main__':unittest.main()
