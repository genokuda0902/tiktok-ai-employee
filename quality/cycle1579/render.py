"""Review-only synthetic 10-genre gate demonstration; no narration or publication approval."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('音声がない動画は','公開しない',0,3),('日本語ナレーション','実音声を確認',3,6),('字幕と音声の同期','未検証なら不合格',6,9),('社員が確認した後に','手動で投稿',9,12)]
def validate(scenes):
    assert scenes and scenes[0][2]==0
    assert all(a<b and (i==0 or a==scenes[i-1][3]) for i,(_,_,a,b) in enumerate(scenes))
def audio_gate(probe,spoken_verified=False,subtitle_sync_verified=False):
    return bool(spoken_verified and subtitle_sync_verified and any(s.get('codec_type')=='audio' for s in probe['streams']))
def render():
    validate(SCENES)
    filters=['drawbox=x=64:y=280:w=952:h=1260:color=0x18263b:t=fill','drawbox=x=64:y=280:w=12:h=1260:color=0x22d3ee:t=fill']
    for h,s,a,b in SCENES:
        alpha=f'if(between(t,{a},{b}),1,0)'
        filters.extend([f"drawtext=fontfile={FONT}:text='{h}':fontsize=70:fontcolor=white:x=(w-text_w)/2:y=630:alpha='{alpha}'",f"drawtext=fontfile={FONT}:text='{s}':fontsize=55:fontcolor=0x67e8f9:x=(w-text_w)/2:y=790:alpha='{alpha}'"])
    filters.extend([f"drawtext=fontfile={FONT}:text='10ジャンル共通・公開前チェック':fontsize=38:fontcolor=0xcbd5e1:x=(w-text_w)/2:y=370",'drawbox=x=120:y=1250:w=840:h=16:color=0x334155:t=fill',"drawbox=x=120:y=1250:w='840*min(t/12,1)':h=16:color=0x22d3ee:t=fill",f"drawtext=fontfile={FONT}:text='REVIEW ONLY / 音声未生成':fontsize=36:fontcolor=0xfbbf24:x=(w-text_w)/2:y=1690"])
    dest=ROOT/'cycle1579_REVIEW_ONLY.mp4'
    with (ROOT/'render.log').open('w') as log:
        subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=c=0x101827:s=1080x1920:r=24:d=12','-vf',','.join(filters),'-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True,stdout=subprocess.DEVNULL,stderr=log)
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
    (ROOT/'probe.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
    assert not audio_gate(p)
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    return dest
if __name__=='__main__':print(render())
