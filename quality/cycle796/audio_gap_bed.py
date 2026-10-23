#!/usr/bin/env python3
"""cycle796: original synthesized ambient bed for silent narration gaps.

No external audio assets, network, proprietary models, or publication actions.
The input MP4 is local review-only media; its license is NOT inferred by this tool.
"""
import argparse
import array
import hashlib
import json
import math
import re
import subprocess
import sys
import wave
from pathlib import Path

GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善', '雑学・科学',
    '旅行・グルメ', '商品比較・暮らし',
)
CHORDS = (
    (110.0, 164.81, 220.0, 329.63),       # Am7
    (87.31, 130.81, 174.61, 261.63),       # Fmaj7
    (130.81, 164.81, 196.00, 261.63),      # Cmaj7
    (98.00, 146.83, 196.00, 246.94),       # G6
)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(map(str,cmd)) + '\n' + p.stderr[-1800:])
    return p


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)


def silence_intervals(source, threshold='-36dB', min_seconds=0.35):
    p = run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(source), '-map', '0:a:0',
             '-af', f'silencedetect=n={threshold}:d={min_seconds}', '-f', 'null', '-'])
    starts = [float(x) for x in re.findall(r'silence_start:\s*([\d.]+)', p.stderr)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*([\d.]+)', p.stderr)]
    return [[a,b] for a,b in zip(starts, ends) if b-a >= min_seconds]


def clamp(x, a=0., b=1.):
    return min(b, max(a, x))


def smoothstep(x):
    x = clamp(x)
    return x*x*(3-2*x)


def gap_envelope(t, gaps):
    # Soft entry/exit to avoid abrupt audible pumping or clicks.
    strength = 0.
    for start, end in gaps:
        if start <= t <= end:
            attack = smoothstep((t-start-0.035)/0.12)
            release = smoothstep((end-t-0.035)/0.12)
            strength = max(strength, min(attack,release))
    return strength


def chord_sample(t, duration):
    # Slow four-chord evolution, continuous phase, crossfaded at boundaries.
    section = duration/4.
    index = min(3, int(t/section))
    within = t - index*section
    def note(chord):
        return sum(math.sin(2*math.pi*f*t + j*0.37) for j,f in enumerate(chord))/4.
    current = note(CHORDS[index])
    if index > 0 and within < 0.75:
        w = smoothstep(within/0.75)
        return (1-w)*note(CHORDS[index-1])+w*current
    return current


def make_original_bed(wav_path, duration, gaps, sample_rate=24000, voice_gain=.005, gap_gain=.070):
    if not (0 < duration <= 180):
        raise ValueError('Duration out of bounds')
    if not (0 <= voice_gain <= .015 and 0 <= gap_gain <= .09):
        raise ValueError('Unsafe background gain')
    n = round(duration*sample_rate)
    pcm = array.array('h')
    for i in range(n):
        t = i/sample_rate
        amp = voice_gain + (gap_gain-voice_gain)*gap_envelope(t,gaps)
        fade = min(smoothstep(t/.55), smoothstep((duration-t)/.75))
        # Original synthesis only; no recorded samples, melody, or borrowed music.
        base = chord_sample(t,duration)
        air = .15*math.sin(2*math.pi*0.19*t)*math.sin(2*math.pi*439.9*t)
        signal = (base+air)*amp*fade
        pcm.append(int(clamp(signal, -1., 1.)*32767))
    wav_path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(wav_path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())
    return {'sample_rate':sample_rate,'samples':n,'gap_gain':gap_gain,'voice_gain':voice_gain,
            'source':'pure_python_synthesis_no_external_audio'}


def video_packet_hash(path):
    p=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-c:v','copy',
           '-f','hash','-hash','sha256','-'])
    return p.stdout.strip()


def pcm_audio(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                      '-ac','1','-ar','16000','-f','f32le','-'],capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1000:])
    data=array.array('f');data.frombytes(p.stdout)
    return data


def audio_delta(a,b):
    x,y=pcm_audio(a),pcm_audio(b)
    n=min(len(x),len(y))
    if abs(len(x)-len(y))>1600:raise ValueError('Audio duration mismatch')
    sq=sum((x[i]-y[i])**2 for i in range(n))/max(1,n)
    return {'rms_delta':round(math.sqrt(sq),6), 'max_delta':round(max(abs(x[i]-y[i]) for i in range(n)),6),
            'samples_compared':n,'sample_rate':16000}


def render(config_path, source, output, report, wav_path):
    config=json.loads(Path(config_path).read_text(encoding='utf8'))
    if config.get('genre') not in GENRES or set(config.get('genres',[])) != set(GENRES):
        raise ValueError('Ten-genre pilot contract mismatch')
    if config.get('mode')!='review_only' or config.get('publication_approved') is not False:
        raise ValueError('This renderer is REVIEW ONLY and must not authorize publication')
    if config.get('rights_reviewed') is not False or config.get('employee_approved') is not False:
        raise ValueError('Rights and employee approval must remain explicitly unverified')
    source=Path(source).resolve();output=Path(output).resolve()
    if not source.is_file():raise FileNotFoundError(source)
    if source == output:raise ValueError('Never overwrite source media')
    if 'REVIEW_ONLY' not in output.name:raise ValueError('Output filename must mark REVIEW_ONLY')
    meta=probe(source)
    v=next((s for s in meta['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in meta['streams'] if s['codec_type']=='audio'),None)
    if not v or not a or v['width']!=1080 or v['height']!=1920:
        raise ValueError('1080x1920 source with audio required')
    duration=float(meta['format']['duration'])
    gaps=silence_intervals(source,config.get('silence_threshold','-36dB'),config.get('min_gap_seconds',.35))
    bed=make_original_bed(Path(wav_path),duration,gaps,gap_gain=config.get('gap_gain',.070),voice_gain=config.get('voice_gain',.005))
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(wav_path),
         '-filter_complex','[0:a:0]aresample=48000,asetpts=PTS-STARTPTS[voice];'
                           '[1:a:0]aresample=48000,asetpts=PTS-STARTPTS[bed];'
                           '[voice][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]',
         '-map','0:v:0','-map','[aout]','-c:v','copy','-c:a','aac','-b:a','192k',
         '-movflags','+faststart',str(output)])
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    outmeta=probe(output)
    outv=next(s for s in outmeta['streams'] if s['codec_type']=='video')
    outa=next(s for s in outmeta['streams'] if s['codec_type']=='audio')
    if outv['width']!=1080 or outv['height']!=1920 or outv['codec_name']!='h264' or outa['codec_name']!='aac':
        raise ValueError('Output codec or resolution mismatch')
    if abs(float(outmeta['format']['duration'])-duration)>.1:
        raise ValueError('Output duration mismatch')
    source_hash=video_packet_hash(source);output_hash=video_packet_hash(output)
    if source_hash!=output_hash:raise ValueError('Video changed unexpectedly')
    delta=audio_delta(source,output)
    if not (.0002 < delta['rms_delta'] < .04 and delta['max_delta'] < .16):
        raise ValueError('Background difference out of safe range: '+str(delta))
    after_gaps=silence_intervals(output,config.get('silence_threshold','-36dB'),config.get('min_gap_seconds',.35))
    qa={'cycle':796,'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED',
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'duration_before':duration,'duration_after':float(outmeta['format']['duration']),
        'video_width':outv['width'],'video_height':outv['height'],'video_frames':outv.get('nb_frames'),
        'video_packet_sha256_unchanged':source_hash==output_hash,'video_packet_sha256':source_hash,
        'audio_codec':outa['codec_name'],'original_voice_retained':True,
        'gap_intervals_before':gaps,'gap_intervals_after':after_gaps,
        'audio_pcm_delta':delta,'bed':bed,
        'speech_content_verified':False,'speech_naturalness_verified':False,
        'caption_semantic_sync_verified':False,'mobile_device_verified':False,
        'reference_v33_compared':False,'asset_rights_verified':False,
        'human_publication_approved':False}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
    return qa


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',required=True);ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--report',required=True)
    ap.add_argument('--bed',required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.config,a.source,a.output,a.report,a.bed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()