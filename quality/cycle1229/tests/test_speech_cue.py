import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from speech_cue import GENRES, PALETTE, frame_rgba, chapter_index, activity_from_pcm, RAIL_W, RAIL_H

class SpeechCueTests(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES),set(PALETTE))
        for genre in GENRES:
            self.assertEqual(len(frame_rgba(.5,True,genre)),RAIL_W*RAIL_H*4)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):frame_rgba(.5,True,'unknown')
    def test_invalid_progress(self):
        with self.assertRaises(ValueError):frame_rgba(1.1,True,'ai')
    def test_frame_has_transparency(self):
        f=frame_rgba(.5,True,'ai')
        self.assertEqual(f[3],0)
        self.assertGreater(f[(5*RAIL_W+100)*4+3],0)
    def test_speech_color_changes(self):
        on=frame_rgba(.5,True,'ai')
        off=frame_rgba(.5,False,'ai')
        self.assertNotEqual(on,off)
    def test_progress_changes(self):
        self.assertNotEqual(frame_rgba(.1,True,'ai'),frame_rgba(.9,True,'ai'))
    def test_chapter_index(self):
        c=[{'start_time':'0','end_time':'1'},{'start_time':'1','end_time':'2'}]
        self.assertEqual(chapter_index(.5,c),0)
        self.assertEqual(chapter_index(1.1,c),1)
    def test_activity_detects_tone_and_silence(self):
        import math
        sr=3000
        samples=[0]*sr+[int(16000*math.sin(2*math.pi*220*i/sr)) for i in range(sr)]
        a,e=activity_from_pcm(samples,sr,60)
        self.assertFalse(any(a[:20]))
        self.assertTrue(all(a[40:55]))
        self.assertGreater(max(e),.2)
    def test_invalid_audio_params(self):
        with self.assertRaises(ValueError):activity_from_pcm([],0,1)

if __name__=='__main__':unittest.main()
