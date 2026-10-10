"""Zero-cost Open JTalk experiment. No publishing or network calls."""
from pathlib import Path
import glob, json, subprocess
LINES=['検討します。その前に、何を聞いた？','安さの説明だけでは、悩みは見えません。','まずは、相手の状況を聞く。','今、何が一番手間ですか？','どれくらい時間がかかりますか？','負担を要約してから、提案へ。']
def main():
 out=Path('output/cycle476');out.mkdir(parents=True,exist_ok=True)
 dic=glob.glob('/var/lib/mecab/dic/open-jtalk/*')[0]
 voice=glob.glob('/usr/share/hts-voice/**/*.htsvoice',recursive=True)[0]
 segments=[]
 for i,line in enumerate(LINES):
  wav=out/f'{i}.wav'
  subprocess.run(['open_jtalk','-x',dic,'-m',voice,'-ow',str(wav)],input=line+'\n',text=True,check=True)
  seg=out/f'{i}_3s.wav'
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(wav),'-af','apad,atrim=duration=3','-ar','48000',str(seg)],check=True)
  segments.append(seg)
 playlist=out/'concat.txt'
 playlist.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in segments))
 subprocess.run(['ffmpeg','-y','-v','error','-safe','0','-f','concat','-i',str(playlist),str(out/'native_ja_narration.wav')],check=True)
 (out/'voice_qa.json').write_text(json.dumps({'auto_post':False,'publication':'NOT_APPROVED'}))
if __name__=='__main__':main()
