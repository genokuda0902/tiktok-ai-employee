"""Speech-band cleanup for Japanese narration (10-genre reusable)."""
import subprocess

def cleanup(source, destination, low_hz=75, high_hz=14500):
    if not 30 <= low_hz < high_hz <= 20000:
        raise ValueError("invalid speech band")
    subprocess.run(["ffmpeg","-hide_banner","-nostdin","-y","-i",str(source),
        "-map","0:v:0","-map","0:a:0","-c:v","copy",
        "-af",f"highpass=f={low_hz},lowpass=f={high_hz}",
        "-c:a","aac","-b:a","192k","-ar","48000",
        "-movflags","+faststart",str(destination)],check=True)
