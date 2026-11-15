import subprocess
import sys


def render(src, dst):
    subprocess.run(['ffmpeg', '-y', '-i', src, '-vf', 'gradfun=strength=0.65:radius=8', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', dst], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


if __name__ == '__main__':
    render(*sys.argv[1:3])
