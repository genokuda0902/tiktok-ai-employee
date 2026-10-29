"""Synthetic-only tests. No private MP4 is committed to GitHub."""
import subprocess, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import audio_loudness as m

class TestPolicy(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRE_POLICIES),10)
        self.assertEqual(m.REVIEWED_GENRES,{'ai_work'})

    def test_unknown_genre_blocked(self):
        with self.assertRaises(ValueError):
            m.render(Path('/missing'),Path('/out'),'a'*64,'not_a_genre')

    def test_unreviewed_genre_blocked(self):
        for genre in set(m.GENRE_POLICIES)-m.REVIEWED_GENRES:
            with self.subTest(genre=genre),self.assertRaises(PermissionError):
                m.render(Path('/missing'),Path('/out'),'a'*64,genre)

    def test_malformed_hash_blocked(self):
        with self.assertRaises(ValueError):
            m.render(Path('/missing'),Path('/out'),'bad')

    def test_source_mismatch_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'s.mp4';p.write_bytes(b'fake')
            with self.assertRaises(PermissionError):
                m.render(p,Path(tmp)/'o.mp4','a'*64)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'s.mp4';p.write_bytes(b'fake')
            with self.assertRaises(ValueError):
                m.render(p,p,m.sha256(p))

    def test_synthetic_video_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'synthetic.mp4';dst=Path(tmp)/'out.mp4'
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
                            'color=c=navy:s=1080x1920:r=30:d=1.2',
                            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.2',
                            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                            '-c:a','aac','-b:a','128k','-shortest',str(src)],
                           check=True,timeout=80)
            report=m.render(src,dst,m.sha256(src))
            self.assertTrue(report['video_bitstream_identical'])
            self.assertFalse(report['publication_approved'])
            self.assertFalse(report['asr_verified'])
            self.assertEqual(report['audio_language_tag'],'jpn')
            self.assertTrue(dst.is_file())

if __name__=='__main__': unittest.main()
