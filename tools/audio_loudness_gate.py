"""Check measured integrated LUFS and true peak on exported MP4 (FFmpeg required)."""
import json
import re
import subprocess
import sys

def measure(path):
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", path, "-af",
         "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    match = re.search(r'\{\s*"input_i".*?\}', result.stderr, re.S)
    if not match:
        raise ValueError("loudnorm measurement missing")
    data = json.loads(match.group())
    return float(data["input_i"]), float(data["input_tp"])

def validate(lufs, true_peak):
    return -17 <= lufs <= -15 and true_peak <= -1.5

if __name__ == "__main__":
    lufs, peak = measure(sys.argv[1])
    print(f"LUFS={lufs}, true_peak_dBTP={peak}, pass={validate(lufs, peak)}")
    sys.exit(0 if validate(lufs, peak) else 1)
