#!/usr/bin/env python3
"""Local-only, SRT-windowed Japanese audio review export. Not ASR or approval.

Outputs 16 kHz mono WAVs and a blank reviewer checklist. Never uploads media.
"""
import argparse
import csv
import json
from pathlib import Path
from caption_panel import parse_srt, run, probe

def export(source,srt,output_dir):
    src=Path(source).resolve();folder=Path(output_dir).resolve()
    if not src.is_file() or folder.exists():raise ValueError('missing source or existing output')
    cues=parse_srt(srt)
    info=probe(src)
    if len([s for s in info['streams'] if s['codec_type']=='audio'])!=1:raise ValueError('one audio track required')
    if abs(float(info['format']['duration'])-cues[-1]['end'])>.045:raise ValueError('SRT duration mismatch')
    folder.mkdir(parents=True)
    rows=[]
    for i,c in enumerate(cues,1):
        filename=f'caption_{i:02d}_listen.wav'
        run(['ffmpeg','-v','error','-y','-ss',f"{c['start']:.3f}",'-i',src,
             '-t',f"{c['end']-c['start']:.3f}",'-map','0:a:0','-ar','16000','-ac','1','-c:a','pcm_s16le',folder/filename])
        rows.append({'index':i,'start':c['start'],'end':c['end'],'expected_caption':' / '.join(c['lines']),
          'wav_file':filename,'listened':'', 'spoken_words_match':'','timing_match':'','pronunciation_ok':'','reviewer_notes':''})
    with (folder/'HUMAN_AUDIO_CHECK.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (folder/'STATUS.json').write_text(json.dumps({'cues':len(cues),'exported_wav':len(rows),
      'audio_review':'PENDING_HUMAN_LISTENING','independent_asr':'NOT_AVAILABLE',
      'semantic_alignment':'NOT_VERIFIED','publication':'NOT_APPROVED'},indent=2),encoding='utf-8')
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--srt',required=True)
    p.add_argument('--out',required=True);a=p.parse_args();print(len(export(a.source,a.srt,a.out)))
