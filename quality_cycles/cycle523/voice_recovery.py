#!/usr/bin/env python3
"""Review-only Japanese narration using free Ubuntu Open JTalk packages."""
from pathlib import Path
import subprocess,glob,wave,json,shutil,array,math
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"/"japanese_voice"
LINES=[
"今日のタスク、全部やろうとしていませんか。",
"やることが多いと、何から始めるか迷います。",
"まずは、成果につながる仕事を選びましょう。",
"次に、期限が今日のものを確認します。",
"最後に、最初の十五分でやることを決めます。",
"今日やる三つが決まれば、迷いが減ります。",
"エーアイには、重要度と期限と最初の一歩を整理して、と伝えます。",
"重要度、期限、最初の十五分。保存して使ってみてください。"]
def first(paths,dir=False):
    for pat in paths:
        for x in glob.glob(pat,recursive=True):
            p=Path(x)
            if (p.is_dir() if dir else p.is_file()):return p
    return None
def prerequisites():
    eng=shutil.which("open_jtalk")
    dic=first(["/var/lib/mecab/dic/open-jtalk/naist-jdic","/usr/share/open-jtalk/dic/naist-jdic","/usr/share/open-jtalk/dic"],dir=True)
    model=first(["/usr/share/hts-voice/**/*.htsvoice","/usr/share/hts-voice/*.htsvoice"])
    if not eng or not dic or not model:raise RuntimeError(f"Japanese TTS unavailable: {eng} {dic} {model}")
    return eng,dic,model
def main():
    eng,dic,model=prerequisites();OUT.mkdir(parents=True,exist_ok=True)
    qa=[]
    for i,line in enumerate(LINES):
        p=OUT/f"voice_{i+1:02}.wav"
        subprocess.run([eng,"-x",str(dic),"-m",str(model),"-r","1.10","-ow",str(p)],input=line+"\n",text=True,check=True)
        with wave.open(str(p),"rb") as f:
            samples=f.readframes(f.getnframes())
            duration=f.getnframes()/f.getframerate()
            rms=math.sqrt(sum(v*v for v in array.array("h",samples))/max(1,len(samples)//2)) if f.getsampwidth()==2 else 0
            if not .4<=duration<=12 or rms<80:raise RuntimeError(f"Invalid Japanese voice segment {i}")
            qa.append({"segment":i+1,"text":line,"duration":round(duration,3),"rms":round(rms,1)})
    (OUT/"voice_qa.json").write_text(json.dumps({"segments":qa,"listening_quality":"HUMAN_REVIEW","publication":"NOT_APPROVED"},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
