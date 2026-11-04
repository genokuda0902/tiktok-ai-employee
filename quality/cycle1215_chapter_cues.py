"""Review-only chapter cues. Not speech transcription."""
CHAPTERS=[(3,6,"目的を明確に"),(6,9,"条件を整理"),(9,12,"結果を確認")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def filtergraph(chapters=CHAPTERS):
    filters=[]
    for start,end,label in chapters:
        if not (0 <= start < end <= 23.033): raise ValueError("invalid chapter time")
        if not label or any(x in label for x in ["'",":","\\","%"]): raise ValueError("unsafe label")
        enable=f"between(t,{start},{end})"
        filters.append(f"drawbox=x=110:y=1390:w=860:h=140:color=black@0.75:t=fill:enable='{enable}'")
        filters.append(f"drawtext=fontfile={FONT}:text='{label}':fontsize=54:fontcolor=white:x=(w-text_w)/2:y=1422:enable='{enable}'")
    return ",".join(filters)
def render(source,output):
    import subprocess
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",filtergraph(),"-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)],check=True)
