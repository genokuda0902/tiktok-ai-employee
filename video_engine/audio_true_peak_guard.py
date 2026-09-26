"""Fail-closed audio delivery checks for short-form masters.

Uses ffmpeg loudnorm analysis output already produced by the render/QA pipeline.
No network or paid service is required.
"""
from __future__ import annotations

def validate_audio_delivery(metrics: dict, *, max_true_peak_dbfs: float = -1.5,
                            min_lufs: float = -19.0, max_lufs: float = -14.0) -> list[str]:
    errors: list[str] = []
    try:
        tp = float(metrics["input_tp"])
        lufs = float(metrics["input_i"])
    except (KeyError, TypeError, ValueError):
        return ["missing_or_invalid_loudness_metrics"]
    if tp > max_true_peak_dbfs:
        errors.append(f"true_peak_too_high:{tp:.2f}>{max_true_peak_dbfs:.2f}")
    if not (min_lufs <= lufs <= max_lufs):
        errors.append(f"integrated_loudness_out_of_range:{lufs:.2f}")
    return errors
