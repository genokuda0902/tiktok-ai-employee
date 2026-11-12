"""Fail closed: an AAC stream or synthetic cue is not Japanese narration."""
def publication_ready(*, has_audio_stream, verified_japanese_speech, captions_speech_aligned, rights_approved, employee_approved):
    return all((has_audio_stream, verified_japanese_speech, captions_speech_aligned, rights_approved, employee_approved))

def review_evidence(*, video_codec, width, height, audio_codec, speech_verified=False, captions_aligned=False):
    return {
        "video_ok": video_codec == "h264" and width == 1080 and height == 1920,
        "audio_stream_present": audio_codec == "aac",
        "japanese_narration_verified": bool(speech_verified),
        "speech_aligned_captions_verified": bool(captions_aligned),
        "publication_approved": False,
    }
