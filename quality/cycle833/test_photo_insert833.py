"""Cycle833 ten-genre safety and synthetic AV integration checks."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from photo_insert833 import PhotoInsert,GENRES,PHOTO_BOX,CTA_TOP,CAPTION_TOP,command,render

class PhotoInsertTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES: PhotoInsert(genre=genre).validate()
    def test_safe_zone(self):
        self.assertLess(PHOTO_BOX[3],CTA_TOP)
        self.assertLess(PHOTO_BOX[3],CAPTION_TOP)
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError): PhotoInsert(genre='invalid').validate()
    def test_caption_overlap_fails(self):
        with self.assertRaises(ValueError): PhotoInsert(box=(0,390,1080,1500)).validate()
    def test_invalid_frames_fail(self):
        with self.assertRaises(ValueError): PhotoInsert(start_frame=101,end_frame=0).validate()
    def test_missing_sources_fail(self):
        with self.assertRaises(FileNotFoundError):
            command(Path('/missing/base.mp4'),Path('/missing/photo.png'),Path('/tmp/out.mp4'))
    def test_hook_frames(self):
        self.assertEqual(PhotoInsert().end_frame,101)
    def test_synthetic_av_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td);base=td/'base.mp4';photo=td/'fictional.ppm';out=td/'out.mp4'
            with photo.open('wb') as f:
                f.write(b'P6\n1024 1536\n255\n')
                for y in range(1536):
                    f.write(bytes((40+(y//35)%90,70+(y//20)%100,110))*1024)
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
                'color=c=0x112233:s=1080x1920:r=30:d=4',
                '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4',
                '-t','4','-c:v','libx264','-preset','ultrafast','-c:a','aac',str(base)],check=True)
            render(base,photo,out)
            info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]))
            v=next(s for s in info['streams'] if s['codec_type']=='video')
            a=next(s for s in info['streams'] if s['codec_type']=='audio')
            self.assertEqual((v['width'],v['height']),(1080,1920))
            self.assertEqual(a['codec_name'],'aac')
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
            self.assertGreater(out.stat().st_size,10000)

if __name__=='__main__': unittest.main()
