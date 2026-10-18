from voice_sync import GENRES, validate_beats, review_status
assert len(GENRES) == 10
assert review_status([1])['publication'] == 'NOT_APPROVED'
assert validate_beats(GENRES[0], [{'start':0,'end':2,'spoken_seconds':1,'caption':'確認','narration':'確認します'}])
