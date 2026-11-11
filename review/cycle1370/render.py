"""Review-only: add real selectable Japanese timed subtitle track to synthetic MP4."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'cycle1369'/'cycle1369_REVIEW_ONLY.mp4'
OUTPUT=ROOT/'cycle1370_REVIEW_ONLY.mp4'
CUES=['毎月の集計、まだ手作業？','架空の売上データを入力','合計セルに SUM 関数を入力','計算結果は270。範囲も確認']
def stamp(t):
 h=int(t//3600);m=int(t//60)%60;s=int(t)%60;ms=int(round((t-int(t))*1000));return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
 if not SOURCE.is_file():raise FileNotFoundError(SOURCE)
 srt=ROOT/'captions.srt'
 srt.write_text(''.join(f'{i+1}\n{stamp(i*2.5)} --> {stamp((i+1)*2.5)}\n{cue}\n\n' for i,cue in enumerate(CUES)),encoding='utf-8')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(SOURCE),'-i',str(srt),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=jpn','-movflags','+faststart',str(OUTPUT)],check=True)
 return OUTPUT
if __name__=='__main__':print(main())
