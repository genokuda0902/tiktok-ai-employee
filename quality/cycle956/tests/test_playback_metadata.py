from __future__ import annotations

import shutil
import subprocess

import pytest
from playback_metadata import (GENRES, REVIEW_SOURCE_SHA, audio_adts_sha,
                               faststart, package, probe, tracks, validate_input,
                               video_frame_hashes)


def test_ten_genres():
    assert len(GENRES) == 10
    assert len(set(GENRES)) == 10
    assert set(REVIEW_SOURCE_SHA) == {"ai_work"}


@pytest.mark.parametrize("genre", ["food", "career", "travel", "health", "technology"])
def test_unreviewed_genres_fail_closed(tmp_path, genre):
    p = tmp_path / "sample.mp4"
    p.write_bytes(b"no private media")
    with pytest.raises(ValueError, match="not reviewed"):
        validate_input(p, genre)


def test_unknown_genre_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="Unsupported"):
        validate_input(tmp_path / "missing.mp4", "not_a_genre")


def test_source_sha_mismatch(tmp_path):
    p = tmp_path / "sample.mp4"
    p.write_bytes(b"incorrect source")
    with pytest.raises(ValueError, match="SHA256 mismatch"):
        validate_input(p, "ai_work")


def test_conflicting_color_policy_guard():
    info = {"streams": [{"codec_type": "video"}, {"codec_type": "audio"}]}
    assert len(tracks(info)) == 2
    with pytest.raises(ValueError):
        tracks({"streams": [{"codec_type": "video"}]})


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="ffmpeg missing")
def test_synthetic_no_reencode_metadata(tmp_path):
    src, dst = tmp_path / "synthetic.mp4", tmp_path / "tagged.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi",
                    "-i", "testsrc2=size=160x288:rate=30:duration=1",
                    "-f", "lavfi", "-i", "sine=frequency=600:sample_rate=48000:duration=1",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src)], check=True)
    package(src, dst)
    v, a = tracks(probe(dst))
    assert (v["color_primaries"], v["color_transfer"], v["color_space"], v["color_range"]) == ("bt709", "bt709", "bt709", "tv")
    assert v["sample_aspect_ratio"] == "1:1"
    assert a["tags"]["language"] == "jpn"
    assert video_frame_hashes(src) == video_frame_hashes(dst)
    assert audio_adts_sha(src) == audio_adts_sha(dst)
    assert faststart(dst)


def test_publication_gate():
    import playback_metadata as mod
    assert not hasattr(mod, "post_to_tiktok")
    assert not hasattr(mod, "merge_pr")
