"""Cycle582 local compositor: synthetic hook + verified cycle581 source.
No external uploads, automatic posting, or Japanese narration claims.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from hook import DEFAULT, FPS, render_frame
from qa_gate import QAResult

SOURCE_SHA256 = '80d20c2b6cf66ed6b18a2e00b1d25b026da999a971302c784d464b15e0cd59b5'
CAPTIONS = ((0,2,'手計算の前に、合計720を確認'),(2,4,'4か月分の売上を入力'),
            (4,6,'SUM関数でも合計720'),(6,9,'数字を入力して集計を指示'),
            (9,12,'B2:B5 を選択する'),(12,16,'グラフの数値も確認'),
            (16,18,'手入力と関数を比較'),(18,19,'保存して、あとで試そう'),
            (19,20,'手計算の前に、合計720を確認'))

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def run(cmd,log):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    Path(log).write_text(' '.join(map(str,cmd))+'\nEXIT '+str(p.returncode)+'\n'+p.stderr)
    if p.returncode: raise RuntimeError(f'command failed: {log}')

def render(source,out):
    source,out=Path(source),Path(out)
    if not source.is_file() or sha(source)!=SOURCE_SHA256:
        raise ValueError('cycle581 SHA mismatch; fail closed')
    out.parent.mkdir(parents=True,exist_ok=True)
    seg=out.parent/'hook_2s.mp4'
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920',
         '-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-crf','20',
         '-pix_fmt','yuv420p',str(seg)]
    with (out.parent/'segment.log').open('w') as log:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for i in range(2*FPS): p.stdin.write(render_frame(DEFAULT,i).tobytes())
        finally: p.stdin.close()
        if p.wait(): raise RuntimeError('hook encoding failed')
    graph=('[1:v]setpts=PTS-STARTPTS[a];'
           '[0:v]trim=start=2:end=20,setpts=PTS-STARTPTS[b];'
           '[a][b]concat=n=2:v=1:a=0,format=yuv420p[v]')
    run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(seg),'-filter_complex',graph,
         '-map','[v]','-map','0:a:0','-map','0:s:0?','-c:v','libx264','-preset','ultrafast',
         '-crf','20','-r','30','-c:a','aac','-b:a','192k','-c:s','mov_text',
         '-t','20','-movflags','+faststart',str(out)],out.parent/'render.log')
    qa=QAResult('ai_productivity',20,CAPTIONS,False,False,False,False).evaluate()
    qa.update(cycle=582,source_sha256=SOURCE_SHA256,output_sha256=sha(out),
              improvement='0-2s original result-first motion graphic with exact 720',
              reference_video_direct_comparison=False,
              audio='inherited BGM/SFX; no Japanese speech',
              content='synthetic data, not real AI execution',cost_jpy=0)
    (out.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output),ensure_ascii=False,indent=2))
