import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]/'source'/'caption_default_guard.py'
spec=importlib.util.spec_from_file_location('caption_default_guard',MODULE)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

class GuardTests(unittest.TestCase):
    def test_ten_genre_registry(self):
        self.assertEqual(len(g.GENRES),10)
        self.assertEqual(g.PRIVATE_TESTED,('ai_work',))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):g.policy('unlisted',True,'0'*64,'/missing','/out')
    def test_reject_unreviewed_genres(self):
        for genre in g.GENRES[1:]:
            with self.subTest(genre=genre),self.assertRaises(ValueError):
                g.policy(genre,True,'0'*64,'/missing','/out')
    def test_reject_publication(self):
        with self.assertRaises(ValueError):g.policy('ai_work',False,'0'*64,'/missing','/out')
    def test_reject_unpinned(self):
        with self.assertRaises(ValueError):g.policy('ai_work',True,'oops','/missing','/out')
    def test_reject_bad_source(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'a';src.write_bytes(b'example')
            with self.assertRaises(ValueError):g.policy('ai_work',True,'0'*64,src,Path(t)/'b')
    def test_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'a';src.write_bytes(b'example')
            with self.assertRaises(ValueError):g.policy('ai_work',True,g.sha256(src),src,src)
    def test_synthetic_remux_disposition(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t);src=t/'synthetic.mp4';out=t/'fixed.mp4';report=t/'report.json';srt=t/'a.srt'
            srt.write_text('1\n00:00:00,000 --> 00:00:01,800\n合成字幕\n',encoding='utf8')
            g.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x122e40:s=1080x1920:r=30:d=2',
                   '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                   '-i',srt,'-map','0:v','-map','1:a','-map','2:s','-t','2',
                   '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-c:s','mov_text',
                   '-metadata:s:a:0','language=jpn','-metadata:s:s:0','language=jpn',src])
            self.assertEqual(g.probe(src)['streams'][2]['disposition']['default'],1)
            result=g.repair(src,out,report,g.sha256(src),review_only=True)
            self.assertEqual(result['after_mp4_subtitle_streams'],0)
            self.assertTrue(result['encoded_video_audio_equal'])
            self.assertEqual(result['sidecar_cues'],1)
            self.assertTrue(out.with_suffix('.srt').exists())
            self.assertTrue(out.exists())
            self.assertEqual(json.loads(report.read_text())['video_decode'],'PASS')
            with self.assertRaises(ValueError):g.repair(src,out,report,g.sha256(src),review_only=True)

if __name__=='__main__':unittest.main()
