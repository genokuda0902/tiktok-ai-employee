#!/usr/bin/env python3
from pathlib import Path
import subprocess, json, wave
O=Path('output'); O.mkdir(exist_ok=True)
voice=O/'narration.wav'; proof=O/'v9_operation.mp4'; out=O/'AI時短ラボ_01_v18.mp4'
with wave.open(str(voice),'rb') as w: D=w.getnframes()/w.getframerate()
fadeout=max(0,D-.25)
fc=f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,
zoompan=z='min(zoom+0.0007,1.08)':d=1:s=1080x1920:fps=30,
drawbox=x=0:y=0:w=iw:h=260:color=0x02091c@0.78:t=fill,
drawbox=x=55:y=90:w=970:h=135:color=0x071b3b@0.92:t=fill,
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='そのExcel、まだ手作業？':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=112:enable='between(t,0,3.2)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='ChatGPTに貼る → 表が完成':fontcolor=0x58eaff:fontsize=55:x=(w-text_w)/2:y=145:enable='between(t,3.2,7.0)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='このままExcelへ':fontcolor=0xffe45e:fontsize=62:x=(w-text_w)/2:y=145:enable='between(t,7.0,13.5)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='コピペ作業を一気に減らす':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=145:enable='between(t,13.5,20.5)',
drawbox=x=70:y=1580:w=940:h=205:color=0x02091c@0.88:t=fill:enable='gte(t,20.5)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='保存して明日使う':fontcolor=0xffe45e:fontsize=68:x=(w-text_w)/2:y=1615:enable='between(t,20.5,26)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='AI時短ラボ':fontcolor=0x58eaff:fontsize=76:x=(w-text_w)/2:y=1600:enable='gte(t,26)',
drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='毎日1つ、仕事がラクになる':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=1700:enable='gte(t,26)',
fade=t=in:st=0:d=0.18,fade=t=out:st={fadeout:.3f}:d=0.25[v]
""".replace('\n','')
subprocess.run(['ffmpeg','-y','-stream_loop','-1','-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','1:a','-t',f'{D:.3f}','-c:v','libx264','-preset','slow','-crf','11','-maxrate','20M','-bufsize','40M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-show_entries','format=duration,size','-of','json',str(out)],text=True))
assert meta['streams'][0]['width']==1080 and meta['streams'][0]['height']==1920
print(json.dumps({'output':str(out),'duration':D,'architecture':'hybrid-studio/no-storyboard-source','meta':meta},ensure_ascii=False))
