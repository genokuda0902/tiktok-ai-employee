import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audio_clarity import PROFILES,filter_chain,command

class AudioClarityTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PROFILES),10)
    def test_profiles_conservative(self):
        for g in PROFILES:
            with self.subTest(genre=g):
                f=filter_chain(g)
                self.assertIn('alimiter=limit=0.88:level=0',f)
                self.assertIn('lowpass=f=14500',f)
    def test_no_unknown_genre(self):
        with self.assertRaises(ValueError):filter_chain('bad')
    def test_video_stream_copy(self):
        c=command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4'))
        self.assertEqual(c[c.index('-c:v')+1],'copy')
    def test_only_two_streams_mapped(self):
        c=command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4'))
        self.assertEqual([c[i+1] for i,x in enumerate(c) if x=='-map'],['0:v:0','0:a:0'])
    def test_no_overwrite_source(self):
        with self.assertRaises(ValueError):command(Path('/tmp/a.mp4'),Path('/tmp/a.mp4'))
    def test_no_external_media(self):
        c=' '.join(command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4')))
        self.assertNotIn('http',c)
    def test_audio_codec(self):
        c=command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4'))
        self.assertEqual(c[c.index('-c:a')+1],'aac')
    def test_audio_sample_rate(self):
        c=command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4'))
        self.assertEqual(c[c.index('-ar')+1],'48000')
    def test_no_autopost(self):
        c=' '.join(command(Path('/tmp/a.mp4'),Path('/tmp/b.mp4')))
        self.assertNotIn('upload',c)
        self.assertNotIn('post',c)
if __name__=='__main__':unittest.main()
