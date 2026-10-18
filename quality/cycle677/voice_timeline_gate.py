"""Reusable Japanese narration timing gate; fail closed for publication."""
def validate(segments, total=20.0):
    if not isinstance(segments, list) or not segments:
        raise ValueError("missing segments")
    previous = 0.0
    for item in segments:
        if set(item) != {"start", "end", "text"}:
            raise ValueError("bad schema")
        start, end = float(item["start"]), float(item["end"])
        if not (0 <= previous <= start < end <= total):
            raise ValueError("overlapping or out-of-bounds speech")
        if not item["text"].strip():
            raise ValueError("empty Japanese narration")
        previous = end
    return True


def validate_measured(segments, measured_seconds, total=20.0):
    validate(segments, total)
    if len(segments) != len(measured_seconds):
        raise ValueError("missing measured voice")
    for segment, seconds in zip(segments, measured_seconds):
        if not (0.15 <= float(seconds) <= float(segment["end"]) - float(segment["start"]) - 0.05):
            raise ValueError("voice is silent or overflows its caption slot")
    return True
