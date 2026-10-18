#!/usr/bin/env python3
"""Cycle671: reusable Japanese caption + optional real narration renderer.
Missing real Japanese speech fails closed. Inherited media rights are NOT assumed.
No TikTok posting, external API, or media upload.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, wave
from pathlib import Path

DURATION=20.0
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
CUES=(
 (0.,2.,'4か月分の合計は？','四か月分の合計は？'),
 (2.,4.,'120、150、200、180','百二十、百五十、二百、百八十。'),
 (4.,6.,'AIに式を相談','エーアイに式を相談。'),
 (6.,8.,'最後は実画面で検証','最後は実画面で検証。'),
 (8.,10.,'=SUM(B2:B5) を入力','サム関数を入力。'),
 (10.,12.4,'数式を入力中','数式を入力中。'),
 (12.4,14.,'合計650を確認','合計六百五十を確認。'),
 (14.,16.,'グラフも4項目で一致','グラフも四項目で一致。'),
 (16.,18.,'手計算と式を比較','手計算と式を比較。'),
 (18.,20.,'保存してあとで試す','保存して、あとで試そう。'),
)
def run(args):
 return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def validate_cues(cues=CUES,duration=DURATION):
 if len(GENRES)!=10 or len(cues)<5:raise ValueError('Genre/cue count invalid')
 if abs(cues[0][0])>.001 or abs(cues[-1][1]-duration)>.001:raise ValueError('Timeline must span full video')
 for i,(start,end,caption,speech) in enumerate(cues):
  if not 0<=start<end<=duration or (i and abs(start-cues[i-1][1])>.001):raise ValueError(f'Gap/overlap at cue {i}')
  if not caption or not speech or len(caption)>22:raise ValueError(f'Caption too long/empty at cue {i}')
 return True
def fmt_srt(t):
 millis=round(t*1000);hh,rem=divmod(millis,3600000);mm,rem=divmod(rem,60000);ss,ms=divmod(rem,1000)
 return f'{hh:02}:{mm:02}:{ss:02},{ms:03}'
def fmt_ass(t):
 cs=round(t*100);hh,rem=divmod(cs,360000);mm,rem=divmod(rem,6000);ss,cs=divmod(rem,100)
 return f'{hh}:{mm:02}:{ss:02}.{cs:02}'
def write_subtitles(outdir,cues=CUES):
 validate_cues(cues);outdir=Path(outdir)
 srt=outdir/'cycle671_scene_timed_NOT_VOICE_SYNCED.srt'
 srt.write_text('\n\n'.join(f'{i}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{cap}' for i,(a,b,cap,_) in enumerate(cues,1))+'\n',encoding='utf-8')
 ass=outdir/'cycle671_burned_caption.ass'
 header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,52,&H00FFFFFF,&H00FFFFFF,&H00091524,&H92091420,1,0,0,0,100,100,0,0,3,13,0,2,100,100,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 events=[]
 for start,end,caption,_ in cues:
  safe=caption.replace('{','').replace('}','').replace('\\','')
  events.append(f'Dialogue: 0,{fmt_ass(start)},{fmt_ass(end)},Caption,,0,0,0,,{{\\fad(100,130)}}{safe}')
 ass.write_text(header+'\n'.join(events)+'\n',encoding='utf-8')
 return srt,ass
def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]).stdout)
def find_openjtalk_assets():
 binary=shutil.which('open_jtalk')
 voices=list(Path('/usr/share/hts-voice').rglob('*.htsvoice')) if Path('/usr/share/hts-voice').exists() else []
 dictionaries=[Path('/var/lib/mecab/dic/open-jtalk/naist-jdic'),Path('/usr/share/open-jtalk/dic'),Path('/usr/share/mecab/dic/open-jtalk/naist-jdic')]
 dic=next((p for p in dictionaries if p.is_dir()),None)
 if not binary or not voices or not dic:raise FileNotFoundError('Open JTalk executable, dictionary or HTS voice missing')
 return binary,dic,voices[0]
def synthesize_voice(outdir,cues=CUES):
 binary,dic,model=find_openjtalk_assets();clips=[]
 for i,(start,end,_,speech) in enumerate(cues):
  wav=Path(outdir)/f'voice_{i:02}.wav'
  subprocess.run([binary,'-x',str(dic),'-m',str(model),'-r','1.20','-ow',str(wav)],input=speech,encoding='utf-8',check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  with wave.open(str(wav),'rb') as f:duration=f.getnframes()/f.getframerate()
  if duration>end-start-.20:raise ValueError(f'Voice overflow at cue {i}: {duration:.3f}s > {end-start-.20:.3f}s')
  clips.append({'file':str(wav),'start':start+.1,'end':start+.1+duration,'duration':duration,'speech':speech})
 return clips
def compose(baseline,output,require_voice=False,rights_approved=False):
 validate_cues();baseline,output=Path(baseline),Path(output)
 if not baseline.is_file():raise FileNotFoundError(baseline)
 meta=probe(baseline);video=next(s for s in meta['streams'] if s['codec_type']=='video')
 if (video['width'],video['height'])!=(1080,1920):raise ValueError('Expected native 1080x1920 baseline')
 if abs(float(meta['format']['duration'])-DURATION)>.05:raise ValueError('Expected 20-second baseline')
 output.parent.mkdir(parents=True,exist_ok=True);srt,ass=write_subtitles(output.parent)
 voice_clips=synthesize_voice(output.parent) if require_voice else []
 if rights_approved and not require_voice:raise ValueError('Release-style render cannot omit verified narration')
 filter_path=str(ass).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(baseline)]
 if voice_clips:
  for c in voice_clips:cmd.extend(['-i',c['file']])
  pieces=['[0:a]volume=0.24[bed]'];labels=['[bed]']
  for i,c in enumerate(voice_clips,1):
   delay=round(c['start']*1000)
   pieces.append(f'[{i}:a]aresample=48000,adelay={delay}|{delay},volume=1.0[v{i}]')
   labels.append(f'[v{i}]')
  pieces.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.88[aout]')
  cmd.extend(['-filter_complex',';'.join(pieces),'-map','0:v:0','-map','[aout]'])
 else:cmd.extend(['-map','0:v:0','-map','0:a:0'])
 cmd.extend(['-vf',f'ass={filter_path}','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a',('aac' if voice_clips else 'copy'),'-movflags','+faststart','-t','20',str(output)])
 run(cmd);result=probe(output)
 v=next(s for s in result['streams'] if s['codec_type']=='video');a=next((s for s in result['streams'] if s['codec_type']=='audio'),None)
 if (v['width'],v['height'])!=(1080,1920) or not a:raise AssertionError('Missing media stream')
 qa={'cycle':671,'input_sha256':sha256(baseline),'output_sha256':sha256(output),'duration':float(result['format']['duration']),'dimensions':[v['width'],v['height']],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'genre':'AI・仕事効率化','genres_supported_by_timeline_contract':len(GENRES),'cues':len(CUES),'caption_kind':('SCENE_TIMED_AND_REAL_VOICE_MEASURED_NOT_HUMAN_REVIEWED' if voice_clips else 'SCENE_TIMED_ONLY_NOT_VOICE_SYNCED'),'voice':('OPENJTALK_GENERATED_NOT_HUMAN_REVIEWED' if voice_clips else 'ABSENT'),'voice_timing':voice_clips,'rights':'APPROVED_ASSERTION_NEEDS_HUMAN_REVIEW' if rights_approved else 'UNVERIFIED_INHERITED_MEDIA','publication':'NOT_APPROVED','post':'MANUAL_ONLY','quality':'HUMAN_REVIEW_ONLY'}
 (output.parent/'cycle671_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
 return qa
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--baseline',required=True);p.add_argument('--output',required=True);p.add_argument('--require-voice',action='store_true');p.add_argument('--rights-approved',action='store_true')
 a=p.parse_args();print(json.dumps(compose(a.baseline,a.output,a.require_voice,a.rights_approved),ensure_ascii=False,indent=2))
