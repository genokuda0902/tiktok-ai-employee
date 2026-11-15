import json,subprocess,unittest
from pathlib import Path
class ReviewTests(unittest.TestCase):
    def test_review_manifest_blocks_publication(self):
        m=json.loads(Path('manifest.json').read_text());self.assertFalse(m['publication_approved']);self.assertFalse(m['narration_present']);self.assertEqual(m['asset_origin'],'synthetic')
    def test_srt_four_segments(self):
        self.assertEqual(Path('captions.srt').read_text().count('-->'),4)
    def test_video_decodes_and_is_vertical(self):
        p='cycle1482_REVIEW_ONLY.mp4'
        x=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))
        v=next(s for s in x['streams'] if s['codec_type']=='video');self.assertEqual((v['width'],v['height']),(720,1280));self.assertFalse(any(s['codec_type']=='audio' for s in x['streams']))
        subprocess.run(['ffmpeg','-v','error','-i',p,'-f','null','-'],check=True)
if __name__=='__main__':unittest.main()
