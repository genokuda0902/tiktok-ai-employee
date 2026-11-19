"""Review-only synthetic caption timeline; no audio and never publish."""
SCENES = [("音声がない動画は","公開しない",0,3),("日本語ナレーション","実音声を確認",3,6),("字幕と音声の同期","未検証なら不合格",6,9),("社員の承認後に","手動で投稿",9,12)]
def validate_scenes(scenes):
    assert scenes and scenes[0][2] == 0
    assert all(a < b and (i == 0 or a == scenes[i-1][3]) for i,(_,_,a,b) in enumerate(scenes))
def publication_approved(has_japanese_voice=False, sync_verified=False, rights_approved=False, employee_approved=False):
    return all([has_japanese_voice, sync_verified, rights_approved, employee_approved])
