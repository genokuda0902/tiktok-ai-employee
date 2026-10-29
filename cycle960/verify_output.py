"""Local-only QA: inspect full private MP4 without uploading it to GitHub."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np


def probe(path):
    p = subprocess.run(['ffprobe','-v','error','-show_entries',
        'format=duration,size:stream=index,codec_name,width,height,r_frame_rate,sample_rate,channels',
        '-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)


def audio_sha(path):
    p = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
        '-c:a','copy','-f','adts','pipe:1'],capture_output=True,check=True)
    return hashlib.sha256(p.stdout).hexdigest()


def inspect(source,output):
    meta = probe(output)
    v = next(x for x in meta['streams'] if x['codec_name']=='h264')
    a = next(x for x in meta['streams'] if x['codec_name']=='aac')
    assert (v['width'],v['height'],v['r_frame_rate']) == (1080,1920,'30/1')
    assert (a['sample_rate'],a['channels']) == ('48000',2)
    assert abs(float(meta['format']['duration'])-691/30)<.03
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True,timeout=120)
    a0,a1=audio_sha(source),audio_sha(output)
    assert a0==a1, 'audio changed'
    cap0,cap1=cv2.VideoCapture(str(source)),cv2.VideoCapture(str(output))
    count=0;max_caption=0;preview_delta=None;outside_max=0
    while True:
        ok0,f0=cap0.read();ok1,f1=cap1.read()
        assert ok0==ok1, 'source/output frame mismatch'
        if not ok0:break
        caption_diff=cv2.absdiff(f0[1490:1840:8,::8],f1[1490:1840:8,::8]).mean()
        max_caption=max(max_caption,float(caption_diff))
        if count==33:
            preview_delta=float(cv2.absdiff(f0[650:850:4,510:870:4],
                                           f1[650:850:4,510:870:4]).mean())
        if count>=90:
            outside_max=max(outside_max,float(cv2.absdiff(f0[::16,::16],f1[::16,::16]).mean()))
        count+=1
    cap0.release();cap1.release()
    assert count==691
    assert max_caption<3, f'caption region changed too much: {max_caption}'
    assert preview_delta is not None and preview_delta>15, f'proof not visible: {preview_delta}'
    assert outside_max<3, f'non-hook video changed too much: {outside_max}'
    return {'frames':count,'duration':float(meta['format']['duration']),
        'video':'h264 1080x1920 30fps','audio':'aac 48000Hz stereo',
        'full_av_decode':'PASS','audio_adts_sha256':a1,'audio_bitstream_equal':'PASS',
        'max_caption_mean_pixel_diff_1of8':round(max_caption,4),
        'preview_mean_pixel_diff_frame33_1of4':round(preview_delta,4),
        'max_outside_hook_diff_1of16':round(outside_max,4),
        'japanese_semantic_asr':'NOT_VERIFIED','phone_playback':'NOT_VERIFIED',
        'publication_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--qa',required=True)
    a=p.parse_args();report=inspect(Path(a.source),Path(a.output))
    Path(a.qa).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
