"""Review-only MP4 subtitle mux. No audio synthesis, no publication."""
import argparse, json, subprocess
from pathlib import Path
CAPTIONS=[("00:00:00,000","00:00:01,500","合計をまだ手入力？"),("00:00:01,500","00:00:05,500","まず合計したい範囲を選択"),("00:00:05,500","00:00:09,500","SUM関数を入力して計算"),("00:00:09,500","00:00:13,500","結果を確認して検算")]
def make_srt():
    return "\n\n".join(f"{i}\n{a} --> {b}\n{t}" for i,(a,b,t) in enumerate(CAPTIONS,1))+"\n"
def mux(source, output):
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    srt=output.with_suffix(".srt"); srt.write_text(make_srt(),encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-i",str(source),"-i",str(srt),"-map","0:v:0","-map","1:0","-c:v","copy","-c:s","mov_text","-metadata:s:s:0","language=jpn","-movflags","+faststart",str(output)],check=True)
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(output)]))
    streams=data["streams"]; video=next(s for s in streams if s["codec_type"]=="video")
    assert (video["width"],video["height"])==(1080,1920)
    assert any(s["codec_type"]=="subtitle" and s["codec_name"]=="mov_text" for s in streams)
    assert not any(s["codec_type"]=="audio" for s in streams)
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--output",required=True);a=p.parse_args();mux(a.source,a.output)
