"""Review-only 10-genre video renderer. No external assets, no private data."""
import json, subprocess, pathlib, argparse
ROOT=pathlib.Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('作業が長い？','まず作業を一つ選ぶ'),('入力は架空データ','個人情報を入れない'),('AIの結果を比較','人が必ず確認する'),('公開前に確認','社員承認後に手動投稿')]
def esc(s):return s.replace('\\','\\\\').replace(':','\\:').replace("'",'’').replace('%','\\%')
def render(out=ROOT/'cycle1471_REVIEW_ONLY.mp4'):
    out=pathlib.Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    parts=[]
    for i,(head,sub) in enumerate(SCENES):
        part=out.parent/f'clip{i}.mp4'
        vf=','.join([f'drawbox=x=44:y=210:w=632:h=850:color=0x15253e:t=fill',f'drawbox=x=44:y=210:w=632:h=8:color=0x4dd8c9:t=fill',f"drawtext=fontfile={BOLD}:text='{esc(head)}':fontsize=47:fontcolor=white:x=(w-text_w)/2:y=360",f"drawtext=fontfile={FONT}:text='{esc(sub)}':fontsize=32:fontcolor=0xd9eaf7:x=(w-text_w)/2:y=535",'drawbox=x=88:y=735:w=544:h=22:color=0x33445d:t=fill',r'drawbox=x=88:y=735:w=544*min(t/3\,1):h=22:color=0x47d4c7:t=fill',f"drawtext=fontfile={FONT}:text='{i+1} / 4':fontsize=27:fontcolor=white:x=(w-text_w)/2:y=925"])
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x0b1427:s=720x1280:r=20:d=3','-vf',vf,'-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-an',str(part)],check=True)
        parts.append(part)
    concat=out.parent/'concat.txt';concat.write_text(''.join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)],cwd=out.parent,check=True)
    def ts(s):return f'00:00:{s:02d},000'
    (out.parent/'captions.srt').write_text(''.join(f'{i+1}\n{ts(i*3)} --> {ts((i+1)*3)}\n{head}\n{sub}\n\n' for i,(head,sub) in enumerate(SCENES)),encoding='utf-8')
    for p in parts:p.unlink()
    concat.unlink()
    return out
if __name__=='__main__':print(render())
