"""Cycle494: original WHY3 storyboard for ten educational genres."""
GENRES = ("ai_workflow","sales","business","psychology","career","beauty","money","science","travel","comparison")
SIZE = (1080,1920)
FPS = 30
SCENE_SECONDS = 3.2
BEATS = 12
SCENE_KEYS = ("question","why_1","why_2","why_3","action","verify")
def is_ready(qa):
    return (
        qa.get("native_ja_voice_reviewed") is True
        and qa.get("decode_ok") is True
        and qa.get("human_approved") is True
        and qa.get("rights_ok") is True
    )
