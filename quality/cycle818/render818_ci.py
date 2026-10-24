"""Cycle818: add animated CTA to inherited cycle817 renderer; review only."""
import argparse,importlib.util
from pathlib import Path
def load_base():
 p=Path(__file__).resolve().parents[1]/'cycle817'/'render817.py'
 spec=importlib.util.spec_from_file_location('r817',p)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def render(root:Path,output:Path,genre='sales_business'):
 m=load_base();orig=m.build_ass
 def add_cta(boundaries,audio,dest):
  phases=orig(boundaries,audio,dest)
  start=max(boundaries[-2],boundaries[-1]-45)
  line=(f'Dialogue: 1,{m.ass_time(start)},{m.ass_time(boundaries[-1])},'
        'Caption,,0,0,0,,{\\an8\\pos(540,1570)\\fad(280,0)'
        '\\bord3\\c&H0067CEFF&}保存して、明日ひとつ試そう\n')
  with Path(dest).open('a',encoding='utf-8') as f:f.write(line)
  return phases
 m.build_ass=add_cta;m.render(root,output,genre)
 (root/'output'/'captions817.ass').rename(root/'output'/'captions818.ass')
 return output
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--root',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--genre',default='sales_business')
 a=p.parse_args();render(a.root,a.output,a.genre)
