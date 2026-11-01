import json,subprocess,tempfile,unittest
from pathlib import Path
from japanese_audio_accessibility import GENRES,POLICY,cues_from_srt,validate,probe,export,sha

SRT='1\n00:00:00,000 --> 00:00:00,900\n最初の作業を選ぶ。\n\n2\n00:00:00,900 --> 00:00:01,800\n結果を人が確認する。\n'

class TestAccessibility(unittest.TestCase):
    def test_all_ten_genres(self):
        data={'streams':[{'codec_type':'video','codec_name':'h264','width':1080,'height':1920,'avg_frame_rate':'30/1','nb_frames':'54'},{'codec_type':'audio','codec_name':'aac','sample_rate':'48000'}],'format':{'duration':'1.8'}}
        for genre in GENRES:
            with self.subTest(genre=genre):self.assertEqual(validate(data,genre),(1.8,54))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate({'streams':[]},'unknown')
    def test_srt_overlap(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'x.srt';p.write_text(SRT);self.assertEqual(len(cues_from_srt(p)),2)
            p.write_text(SRT.replace('00:00:00,900 --> 00:00:01,800','00:00:00,800 --> 00:00:01,800'))
            with self.assertRaises(ValueError):cues_from_srt(p)
    def test_synthetic_integration(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t);src=d/'src.mp4';out=d/'out.mp4';srt=d/'captions.srt';srt.write_text(SRT)
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=blue:s=1080x1920:r=30:d=1.8',
                            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.8',
                            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)],check=True)
            manifest=d/'manifest.json'
            manifest.write_text(json.dumps({'policy':POLICY,'source_sha256':sha(src),'genre':'ai','asset_approval':'review_only_no_public_rights_claim'}))
            result=export(src,out,srt,d/'qa.json',manifest)
            self.assertEqual(result['audio_language'],'jpn')
            self.assertTrue(result['video_elementary_unchanged'])
            self.assertTrue(result['audio_elementary_unchanged'])
            self.assertEqual(len(result['speech_caption_timing_audit']['cues']),2)
            self.assertEqual(probe(out)['streams'][1]['tags']['language'],'jpn')
            with self.assertRaises(FileExistsError):export(src,out,srt,d/'qa2.json',manifest)
            manifest.write_text('{}')
            with self.assertRaises(ValueError):export(src,d/'new.mp4',srt,d/'qa3.json',manifest)

if __name__=='__main__':unittest.main()
