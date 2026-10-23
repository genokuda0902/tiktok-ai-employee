"""Run cycle782 progress-rail renderer. No media is uploaded or published."""
import argparse
import json
import subprocess
from pathlib import Path
from guard import check, digest
from rail import overlay

def render(source, manifest, output, qa):
    m, info = check(source, manifest)
    output, qa = Path(output), Path(qa)
    output.parent.mkdir(parents=True, exist_ok=True)
    qa.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(source), "-vf", overlay(m["beats"]),
                    "-map", "0:v:0", "-map", "0:a:0", "-map", "0:s:0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-c:s", "copy",
                    "-movflags", "+faststart", str(output)], check=True)
    report = {"cycle": 782, "genre": m["genre_id"],
              "input_sha256": digest(source), "output_sha256": digest(output),
              "publication_approved": False, "speech_content_verified": False,
              "caption_semantics_verified": False, "rights_verified": False}
    (qa / "report.json").write_text(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for key in ("source", "manifest", "output", "qa"):
        p.add_argument("--" + key, required=True)
    a = p.parse_args()
    print(json.dumps(render(a.source, a.manifest, a.output, a.qa), indent=2))
