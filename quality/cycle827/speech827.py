"""Cycle827: offline Japanese speech-activity-aware ASS captions; review-only.
This is NOT forced alignment or proof of accurate Japanese pronunciation.
All imagery/voice is produced by existing cycle826/cycle819 code.
"""
from __future__ import annotations
import json,re,subprocess,sys
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"cycle826"))
import cycle826 as prev
FPS=30
FRAMES=prev.FRAMES
SPEECH=prev.SPEECH
PHRASES=[list(x) for x in prev.PHRASES]
PHRASES[1]=['まず、','繰り返している作業を','書き出す。']
PHRASES[2]=['次に、','完成形の見本を','用意する。']
PHRASES[3]=['指示は、','目的と条件を具体的に','伝える。']
assert len(PHRASES)==8 and sum(FRAMES)==775
assert all(''.join(x)==s for x,s in zip(PHRASES,SPEECH))

def silence_intervals(audio,total):
    p=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(audio),'-af',
      'silencedetect=noise=-38dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    starts=[float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)',p.stderr)]
    ends=[float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)',p.stderr)]
    return [(max(0,a),min(total,ends[i] if i<len(ends) else total))
            for i,a in enumerate(starts) if (ends[i] if i<len(ends) else total)>a]

def active_spans(lo,hi,silences):
    spans=[];cursor=lo
    for a,b in silences:
        if b<=lo or a>=hi:continue
        a=max(a,lo);b=min(b,hi)
        if a>cursor:spans.append((cursor,a))
        cursor=max(cursor,b)
    if cursor<hi:spans.append((cursor,hi))
    return [(a,b) for a,b in spans if b-a>=0.03]

def active_quantile(spans,q):
    total=sum(b-a for a,b in spans)
    if not total:return None
    remaining=q*total
    for a,b in spans:
        if remaining<=(b-a)+1e-9:return a+min(remaining,b-a)
        remaining-=b-a
    return spans[-1][1]

def align_scene(lo,hi,parts,silences):
    spans=active_spans(lo,hi,silences)
    if not spans:return [lo,lo+(hi-lo)/3,lo+2*(hi-lo)/3,hi],False,spans
    weights=[sum(c not in '、。！？・「」 ' for c in p) for p in parts]
    cumulative=[weights[0]/sum(weights),(weights[0]+weights[1])/sum(weights)]
    bounds=[active_quantile(spans,q) for q in cumulative]
    for j,t in enumerate(bounds):
        for a,b in silences:
            if b-a>=0.16 and lo+0.2<b<hi-0.18 and a-0.12<=t<=b+0.09:
                bounds[j]=b;break
    first=max(lo,min(spans[0][0],hi-6/FPS))
    b1=max(first+2/FPS,min(bounds[0],hi-4/FPS))
    b2=max(b1+2/FPS,min(bounds[1],hi-2/FPS))
    return [first,b1,b2,hi],True,spans

def timestamp(seconds):
    cs=int((Decimal(str(seconds))*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    return f'{cs//360000}:{(cs//6000)%60:02}:{(cs//100)%60:02}.{cs%100:02}'

def create(root):
    root=Path(root);out=root/'output';out.mkdir(parents=True,exist_ok=True)
    silences=silence_intervals(root/'source'/'voice.m4a',775/FPS)
    lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 2',
      '[V4+ Styles]',
      'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
      'Style: Caption,Noto Sans CJK JP,65,&H00FFFFFF,&H00FFFFFF,&H000A2638,&HAA000000,-1,0,0,0,100,100,0,0,1,5,1,5,65,65,0,1',
      '[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    details=[];frame=0
    for i,(parts,n) in enumerate(zip(PHRASES,FRAMES)):
        lo,hi=frame/FPS,(frame+n)/FPS
        bounds,detected,spans=align_scene(lo,hi,parts,silences)
        old=[lo,lo+n/FPS/3,lo+2*n/FPS/3,hi]
        for phase in range(3):
            colored=[r'{\c'+('&H006BEBD9&' if j==phase else '&H00FFFFFF&')+'}'+p for j,p in enumerate(parts)]
            text=r'{\an5\pos(540,1540)\fad(90,0)}'+r'\N'.join(colored)
            lines.append(f'Dialogue: 0,{timestamp(bounds[phase])},{timestamp(bounds[phase+1])},Caption,,0,0,0,,{text}')
        details.append({'scene':i+1,'voice_activity_detected':detected,
          'active_spans_sec':[[round(a,3),round(b,3)] for a,b in spans],
          'caption_boundaries_sec':[round(x,3) for x in bounds],
          'old_equal_thirds_sec':[round(x,3) for x in old],
          'shift_from_old_sec':[round(bounds[j]-old[j],3) for j in (1,2)]})
        frame+=n
    (out/'captions827.ass').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    result={'cycle':827,'previous_cycle':826,'method':'silencedetect -38dB/0.12s plus active-speech character-weighted heuristic',
      'not_forced_alignment':True,'manual_listening_required':True,'genre_independent':True,
      'scene_count':8,'caption_states':24,
      'silence_intervals_sec':[[round(a,3),round(b,3)] for a,b in silences],
      'scenes':details,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    (out/'sync827.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',required=True,type=Path)
    print(json.dumps(create(p.parse_args().root),ensure_ascii=False,indent=2))
