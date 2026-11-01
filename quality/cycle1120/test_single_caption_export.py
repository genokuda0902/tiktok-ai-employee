import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('single_caption_export',Path(__file__).with_name('single_caption_export.py'))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class SingleCaptionExportTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(mod.GENRES),10)
        self.assertEqual(len(set(mod.GENRES)),10)
    def test_unknown_genre(self):
        with self.assertRaisesRegex(ValueError,'unknown genre'):
            mod.export(Path('x'),Path('y'),Path('z'),Path('w'),'none','unknown')
    def test_paths_cannot_overlap(self):
        with self.assertRaisesRegex(ValueError,'paths must differ'):
            mod.export(Path('x'),Path('x'),Path('z'),Path('w'),'none')
    def test_missing_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with self.assertRaisesRegex(ValueError,'SRT sidecar'):
                mod.export(p/'source',p/'out',p/'missing.srt',p/'report','none')
    def test_media_rules(self):
        data={'streams':[{'codec_type':'video','codec_name':'h264','width':1080,'height':1920,'avg_frame_rate':'30/1','nb_frames':'60'}, {'codec_type':'audio','codec_name':'aac','sample_rate':'48000'}, {'codec_type':'subtitle','codec_name':'mov_text'}],'format':{'duration':'2'}}
        self.assertEqual(mod.check_media(data),(2.0,60,1))
        data['streams'][0]['width']=720
        with self.assertRaisesRegex(ValueError,'dimensions'):mod.check_media(data)
    def test_synthetic_full_roundtrip_and_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);base=p/'base.mp4';withsoft=p/'soft.mp4';side=p/'captions.srt';out=p/'single.mp4';report=p/'qa.json'
            side.write_text('1\n00:00:00,000 --> 00:00:01,200\n架空の例です。\n',encoding='utf-8')
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=navy:s=1080x1920:r=30:d=1.2','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.2','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(base)],check=True)
            subprocess.run(['ffmpeg','-v','error','-i',str(base),'-i',str(side),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text',str(withsoft)],check=True)
            self.assertEqual(mod.check_media(mod.inspect(withsoft))[2],1)
            with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
                mod.export(withsoft,out,side,report,'bad')
            result=mod.export(withsoft,out,side,report,mod.digest(withsoft),expected=(1080,1920))
            self.assertEqual(result['output_soft_subtitle_tracks'],0)
            self.assertEqual(result['full_av_decode'],'PASS')
            self.assertEqual(result['spoken_Japanese_ASR'],'NOT VERIFIED')
            self.assertEqual(json.loads(report.read_text())['frames'],36)
            with self.assertRaises(FileExistsError):mod.export(withsoft,out,side,report,mod.digest(withsoft))
if __name__=='__main__':unittest.main()
