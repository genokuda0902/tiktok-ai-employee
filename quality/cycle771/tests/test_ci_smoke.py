"""Standalone stdlib + ffmpeg smoke test for GitHub Actions; no external media needed."""
import json,struct,subprocess,sys,tempfile,unittest,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from compositor import compose,read_cues,write_ass,DEFAULT_CUTS

def chunk(name,payload):
    return struct.pack('>I',len(payload))+name+payload+struct.pack('>I',zlib.crc32(name+payload)&0xffffffff)

def png(path,color):
    w,h=1080,1920
    raw=(b'\x00'+bytes(color)*w)*h
    payload=zlib.compress(raw,6)
    Path(path).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',payload)+chunk(b'IEND',b''))

class CoreTests(unittest.TestCase):
    def test_cut_length(self):self.assertEqual(DEFAULT_CUTS[-1],429)
    def test_srt_parser(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.srt';p.write_text('1\n00:00:00,167 --> 00:00:01,000\nこの基板、\n',encoding='utf8')
            self.assertEqual(read_cues(p)[0][2],'この基板、')
    def test_ass_safe_position(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.ass';write_ass([('00:00:00,000','00:00:01,000','日本語')],p)
            self.assertIn('\\pos(540,1585)',p.read_text())
    def test_synthetic_mp4(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td);(r/'assets').mkdir();(r/'config').mkdir()
            for i in range(8):png(r/'assets'/f'slide_{i+1:02}.png',(5+i*6,27+i*5,42+i*4))
            (r/'config/phrase_cues.srt').write_text('1\n00:00:00,000 --> 00:00:14,200\n日本語字幕\n',encoding='utf8')
            audio=r/'voice.m4a'
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','sine=frequency=440:duration=14.314','-c:a','aac','-ar','48000',str(audio)],check=True)
            output=compose(r,audio,r/'test.mp4')
            info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames','-of','json',str(output)]))
            self.assertEqual(info['streams'][0]['width'],1080)
            self.assertEqual(info['streams'][0]['height'],1920)
            self.assertEqual(int(info['streams'][0]['nb_frames']),429)
            self.assertEqual(info['streams'][1]['codec_name'],'aac')
            subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)

if __name__=='__main__':unittest.main()
