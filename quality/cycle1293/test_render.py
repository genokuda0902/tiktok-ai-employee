import json, subprocess, unittest
from pathlib import Path
class TestReviewOutput(unittest.TestCase):
    def test_review_render(self):
        root=Path(__file__).resolve().parent
        subprocess.run(['python',str(root/'render.py')],check=True)
        p=root/'cycle1293_REVIEW_ONLY.mp4'
        data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=codec_type,width,height','-of','json',str(p)]))
        self.assertEqual(round(float(data['format']['duration'])),9)
        video=next(s for s in data['streams'] if s['codec_type']=='video')
        self.assertEqual((video['width'],video['height']),(1080,1920))
        self.assertFalse(any(s['codec_type']=='audio' for s in data['streams']))
        subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
if __name__=='__main__': unittest.main()
