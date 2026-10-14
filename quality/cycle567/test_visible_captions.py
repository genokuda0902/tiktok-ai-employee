#!/usr/bin/env python3
"""cycle567 quality gates: unit and optional real-MP4 integration tests."""
import os, subprocess, tempfile, unittest
from pathlib import Path
from render_visible_captions import CUES, PANEL, VIDEO, make_ass, ts

SOURCE = Path(os.environ['CYCLE567_SOURCE']) if os.environ.get('CYCLE567_SOURCE') else None
OUTPUT = Path(os.environ['CYCLE567_OUTPUT']) if os.environ.get('CYCLE567_OUTPUT') else None

def ff(*args):
    return subprocess.check_output(['ffmpeg','-v','error',*map(str,args)],stderr=subprocess.STDOUT)

def probe(path):
    import json
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

class CaptionUnitTests(unittest.TestCase):
    def test_eight_nonoverlapping_cues(self):
        self.assertEqual(len(CUES),8)
        self.assertEqual(CUES[0][0],0)
        self.assertEqual(CUES[-1][1],20)
        self.assertTrue(all(CUES[i][1]==CUES[i+1][0] for i in range(7)))

    def test_safe_panel(self):
        x0,y0,x1,y1=PANEL
        self.assertTrue(0<=x0<x1<=VIDEO[0])
        self.assertTrue(1600<y0<y1<=1800)
        self.assertTrue(all(len(s)<=26 for _,_,s in CUES))

    def test_ass_is_japanese_and_not_fake_transcript(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cues.ass';make_ass(p)
            s=p.read_text(encoding='utf8')
            self.assertIn('SUMの範囲を確認',s)
            self.assertIn('VISUAL STEP 01/08',s)
            self.assertEqual(s.count('Dialogue:'),24)
            self.assertNotIn('ナレーションを読み上げ',s)

    def test_ass_timestamps(self):
        self.assertEqual(ts(0),'0:00:00.00')
        self.assertEqual(ts(15.5),'0:00:15.50')

@unittest.skipUnless(SOURCE and OUTPUT and SOURCE.exists() and OUTPUT.exists(), 'media integration requires actual MP4s')
class CaptionIntegrationTests(unittest.TestCase):
    def test_streams_duration_resolution(self):
        d=probe(OUTPUT); v=next(x for x in d['streams'] if x['codec_type']=='video')
        self.assertEqual((v['width'],v['height']),VIDEO)
        self.assertEqual(int(v['nb_frames']),600)
        self.assertAlmostEqual(float(d['format']['duration']),20,places=2)
        self.assertEqual({x['codec_type'] for x in d['streams']},{'video','audio','subtitle'})

    def test_full_decode(self):
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(OUTPUT),'-map','0:v:0','-f','null','-'],check=True,stdout=subprocess.DEVNULL)

    def test_audio_and_soft_subtitles_bitstream_unchanged(self):
        for stream in ('a','s'):
            a=ff('-i',SOURCE,'-map',f'0:{stream}:0','-c','copy','-f','md5','-')
            b=ff('-i',OUTPUT,'-map',f'0:{stream}:0','-c','copy','-f','md5','-')
            self.assertEqual(a,b)

    def test_upper_content_preserved_and_caption_panel_visible(self):
        def frame(p,t,filter_):
            return ff('-ss',t,'-i',p,'-frames:v','1','-vf',filter_,'-f','rawvideo','-')
        upper='crop=1080:1600:0:0,scale=108:160,format=gray'
        panel='crop=980:150:50:1625,scale=98:15,format=gray'
        a=frame(SOURCE,'10.5',upper); b=frame(OUTPUT,'10.5',upper)
        self.assertLess(sum(abs(x-y) for x,y in zip(a,b))/len(a),2.5)
        for t in ('1','3','5','7.5','10.5','13.5','17','19'):
            a=frame(SOURCE,t,panel); b=frame(OUTPUT,t,panel)
            self.assertGreater(sum(abs(x-y) for x,y in zip(a,b))/len(a),5,t)

if __name__=='__main__': unittest.main(verbosity=2)
