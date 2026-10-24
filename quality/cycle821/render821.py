"""Cycle821 review-only renderer: mobile-safe three-line Japanese karaoke.
Reuses cycle817 original-image renderer; no external services or auto-posting.
"""
from pathlib import Path
import argparse,importlib.util
from PIL import Image,ImageDraw

BASE=Path(__file__).resolve().parents[1]/"cycle817"/"render817.py"
spec=importlib.util.spec_from_file_location("render817_cycle821",BASE)
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

def render(root:Path,output:Path,genre="sales_business"):
 original_ass=base.build_ass
 original_clean=base.clean_slide
 def clean_no_pill(source,dest,accent):
  original_clean(source,dest,accent)
  im=Image.open(dest).convert("RGB")
  ImageDraw.Draw(im).rectangle((90,1210,330,1290),fill=(5,23,39))
  im.save(dest,optimize=True)
 def captions(boundaries,audio,dest):
  phases=original_ass(boundaries,audio,dest)
  s=Path(dest).read_text(encoding="utf8")
  assert s.count("Dialogue:")==24
  s=s.replace("Sans CJK JP,80,","Sans CJK JP,90,")
  s=s.replace(r"\pos(540,1300)",r"\pos(540,1235)\fad(110,0)")
  lines=s.splitlines()
  for i,line in enumerate(lines):
   if not line.startswith("Dialogue:") or r"\pos(540,1235)" not in line:continue
   marker=r"{\c&H00"
   positions=[j for j in range(len(line)) if line.startswith(marker,j)]
   if len(positions)!=3:raise AssertionError("Expected 3 color-coded phrases")
   lines[i]=line[:positions[2]]+r"\N"+line[positions[2]:]
  s="\n".join(lines)+"\n"
  start=max(boundaries[-2],boundaries[-1]-45)
  s+=f'Dialogue: 1,{base.ass_time(start)},{base.ass_time(boundaries[-1])},Caption,,0,0,0,,{{\\an8\\pos(540,1590)\\fad(260,0)\\fs52\\bord3\\c&H0067CEFF&}}保存して、明日ひとつ試そう\n'
  Path(dest).write_text(s,encoding="utf8")
  return phases
 base.build_ass=captions
 base.clean_slide=clean_no_pill
 try:return base.render(root,output,genre)
 finally:
  base.build_ass=original_ass
  base.clean_slide=original_clean

if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--root",type=Path,required=True)
 p.add_argument("--output",type=Path,required=True)
 p.add_argument("--genre",default="sales_business")
 a=p.parse_args();print(render(a.root,a.output,a.genre))
