"""Free Linux Japanese voice feasibility test. REVIEW_ONLY, not publication QA.
Creates a 6s technical MP4 only if real open_jtalk Japanese voice succeeds.
"""
from pathlib import Path
import subprocess,json,hashlib,shutil,os
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'ci_output'
OUT.mkdir(exist_ok=True)
def run(cmd,log,input=None):
    p=subprocess.run(cmd,input=input,text=True,capture_output=True)
    (OUT/log).write_text(' '.join(cmd)+'\n'+p.stdout+'\n'+p.stderr,encoding='utf8')
    if p.returncode:raise RuntimeError(log+': '+p.stderr[-500:])
    return p
def main():
    voice=next(iter(Path('/usr/share/hts-voice').rglob('*.htsvoice')),None)
    dic=Path('/var/lib/mecab/dic/open-jtalk/naist-jdic')
    if not voice or not dic.exists() or not shutil.which('open_jtalk'):
        raise RuntimeError('Japanese TTS unavailable; do not mark as narrated')
    speech='売上データを整理して、グラフにします。最後は人が数字を確認しましょう。'
    run(['open_jtalk','-x',str(dic),'-m',str(voice),'-ow',str(OUT/'ja.wav')],'tts.log',speech)
    if (OUT/'ja.wav').stat().st_size<10000:raise RuntimeError('Japanese voice too small')
    font=next(iter(Path('/usr/share/fonts').rglob('NotoSansCJK-Regular.ttc')),None)
    if not font:raise RuntimeError('Japanese font unavailable')
    (OUT/'caption.txt').write_text('AIで整理 → 人が検算',encoding='utf8')
    draw='drawtext=fontfile='+str(font)+':textfile='+str(OUT/'caption.txt')+':fontcolor=white:fontsize=46:x=(w-text_w)/2:y=540:box=1:boxcolor=0x142e50@0.9:boxborderw=24'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x102a48:s=720x1280:r=30:d=6','-i',str(OUT/'ja.wav'),'-vf',draw,'-filter_complex','[1:a]apad,atrim=0:6[a]','-map','0:v','-map','[a]','-t','6','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(OUT/'ja_voice_technical_REVIEW_ONLY.mp4')],'encode.log')
    run(['ffmpeg','-v','error','-i',str(OUT/'ja_voice_technical_REVIEW_ONLY.mp4'),'-f','null','-'],'decode.log')
    m={'technical_smoke':True,'japanese_tts_engine':'open_jtalk','voice_file':str(voice),'publication_approved':False,'speech_caption_sync':'NOT_VERIFIED','sha256':hashlib.sha256((OUT/'ja_voice_technical_REVIEW_ONLY.mp4').read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
