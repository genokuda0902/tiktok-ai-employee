"""Review-only, no-reencode MP4 packaging for image-first Japanese slides.

Only an exact, private SHA-locked AI-work source is currently accepted. BT.709 is
an explicit *HD SDR assumption*, NOT proven source colorimetry. Fail closed for
unapproved genres, conflicting source tags, codecs, or dimensions. Never posts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ("ai_work", "work_skills", "finance", "career", "education",
          "health", "lifestyle", "travel", "food", "technology")
# Source media itself is NEVER stored in the public repository.
REVIEW_SOURCE_SHA = {"ai_work": "07b9442a73ac4b03de9c2b2e8512f5448690a54660e5391b6b97a5c52646de28"}
EXPECTED_FRAMES = 691


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def run(*args: str, capture: bool = True) -> str:
    p = subprocess.run(args, check=True, capture_output=capture, text=capture)
    return p.stdout if capture else ""


def probe(path: Path) -> dict:
    return json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)))


def tracks(info: dict) -> tuple[dict, dict]:
    videos = [s for s in info["streams"] if s["codec_type"] == "video"]
    audios = [s for s in info["streams"] if s["codec_type"] == "audio"]
    if len(videos) != 1 or len(audios) != 1:
        raise ValueError("Expected exactly one video and one audio stream")
    return videos[0], audios[0]


def validate_input(path: Path, genre: str) -> tuple[dict, str]:
    if genre not in GENRES:
        raise ValueError("Unsupported genre")
    if genre not in REVIEW_SOURCE_SHA:
        raise ValueError("Genre source not reviewed; fail closed")
    digest = sha256_file(path)
    if digest != REVIEW_SOURCE_SHA[genre]:
        raise ValueError("Private source SHA256 mismatch; fail closed")
    info = probe(path)
    v, a = tracks(info)
    if (v.get("codec_name"), v.get("pix_fmt"), v.get("width"), v.get("height"),
        v.get("r_frame_rate"), int(v.get("nb_frames", -1))) != ("h264", "yuv420p", 1080, 1920, "30/1", EXPECTED_FRAMES):
        raise ValueError("Unexpected video parameters")
    if a.get("codec_name") != "aac" or a.get("sample_rate") != "48000":
        raise ValueError("Unexpected audio parameters")
    # Never overwrite a known different transfer function/primaries/matrix.
    for key in ("color_primaries", "color_transfer", "color_space"):
        if v.get(key) not in (None, "unknown", "bt709"):
            raise ValueError(f"Conflicting color tag {key}={v[key]}")
    if v.get("color_range") not in (None, "unknown", "tv"):
        raise ValueError("Conflicting color range")
    return info, digest


def package(source: Path, output: Path) -> None:
    """No re-encoding: rewrite H264 VUI, set Japanese track, preserve AAC packets."""
    output.parent.mkdir(parents=True, exist_ok=True)
    run("ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(source),
        "-map", "0:v:0", "-map", "0:a:0", "-c", "copy",
        "-bsf:v", "h264_metadata=sample_aspect_ratio=1/1:video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
        "-metadata:s:a:0", "language=jpn", "-movflags", "+faststart", str(output))


def video_frame_hashes(path: Path) -> list[str]:
    result = run("ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                 "-map", "0:v:0", "-f", "framemd5", "-")
    return [line.rsplit(",", 1)[-1].strip() for line in result.splitlines() if line and not line.startswith("#")]


def audio_adts_sha(path: Path) -> str:
    proc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
                             "-map", "0:a:0", "-c:a", "copy", "-f", "adts", "-"],
                            stdout=subprocess.PIPE)
    h = hashlib.sha256()
    assert proc.stdout is not None
    for chunk in iter(lambda: proc.stdout.read(1 << 20), b""):
        h.update(chunk)
    if proc.wait() != 0:
        raise RuntimeError("AAC extraction failed")
    return h.hexdigest()


def faststart(path: Path) -> bool:
    with path.open("rb") as f:
        head = f.read(1 << 18)
    return 0 <= head.find(b"moov") < head.find(b"mdat")


def verify(source: Path, output: Path) -> dict:
    src, dst = probe(source), probe(output)
    sv, _ = tracks(src)
    dv, da = tracks(dst)
    hashes_before, hashes_after = video_frame_hashes(source), video_frame_hashes(output)
    audio_before, audio_after = audio_adts_sha(source), audio_adts_sha(output)
    if hashes_before != hashes_after or len(hashes_after) != EXPECTED_FRAMES:
        raise RuntimeError("Decoded video frames changed or were dropped")
    if audio_before != audio_after:
        raise RuntimeError("Original AAC packets changed")
    if (dv.get("color_primaries"), dv.get("color_transfer"), dv.get("color_space"),
        dv.get("color_range"), dv.get("sample_aspect_ratio")) != ("bt709", "bt709", "bt709", "tv", "1:1"):
        raise RuntimeError("Missing target video metadata")
    if da.get("tags", {}).get("language") != "jpn":
        raise RuntimeError("Missing Japanese audio language tag")
    if not faststart(output):
        raise RuntimeError("MP4 moov is not ahead of mdat")
    run("ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(output), "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-")
    return {
        "source_sha256": sha256_file(source), "output_sha256": sha256_file(output),
        "frames": len(hashes_after), "duration_s": float(dst["format"]["duration"]),
        "video": {"codec": dv["codec_name"], "width": dv["width"], "height": dv["height"],
                  "fps": dv["r_frame_rate"], "color_primaries": dv["color_primaries"],
                  "color_transfer": dv["color_transfer"], "color_space": dv["color_space"],
                  "color_range": dv["color_range"], "sample_aspect_ratio": dv["sample_aspect_ratio"]},
        "audio": {"codec": da["codec_name"], "sample_rate": da["sample_rate"],
                  "channels": da["channels"], "language_tag": da["tags"]["language"],
                  "adts_sha256": audio_after, "packet_stream_identical": True},
        "decoded_video_frames_identical": True, "faststart": True, "full_av_decode": "PASS",
        "source_colorimetry": {k: sv.get(k, "UNSPECIFIED") for k in ("color_primaries", "color_transfer", "color_space", "color_range")},
        "color_assumption": "PROVISIONAL: HD SDR BT.709 inferred; master colorimetry not verified",
        "japanese_speech_transcription": "UNVERIFIED", "subtitle_semantic_timing": "UNVERIFIED",
        "source_asset_rights": "UNVERIFIED", "smartphone_playback": "UNVERIFIED",
        "reference_v33_original": "UNAVAILABLE", "human_approval": False,
        "publication_approved": False, "automated_posting": False,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--genre", choices=GENRES, default="ai_work")
    p.add_argument("--assume-hd-sdr-bt709", action="store_true", required=True,
                   help="Explicitly opt into provisional HD SDR BT.709 metadata for review ONLY")
    p.add_argument("--qa", type=Path)
    args = p.parse_args()
    validate_input(args.source, args.genre)
    package(args.source, args.output)
    report = verify(args.source, args.output)
    if args.qa:
        args.qa.parent.mkdir(parents=True, exist_ok=True)
        args.qa.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
