import subprocess, sys

def command(source, target):
    return ['ffmpeg','-y','-v','error','-i',source,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',target]

if __name__ == '__main__':
    subprocess.run(command(*sys.argv[1:]),check=True)
