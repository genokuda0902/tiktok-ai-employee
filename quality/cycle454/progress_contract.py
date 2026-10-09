"""Cycle454 reusable 3-step proof progress timeline. Review only."""
DURATION = 20.0
PHASES = (("01 発見", 0.0, 8.0), ("02 抽出", 8.0, 14.0), ("03 確認", 14.0, 20.0))
VOICE_SEGMENTS = (
    (0, 2, "八件のうち、未対応は二件。"),
    (2, 5, "まず一覧の対応状況を確認します。"),
    (5, 8, "赤く表示された未対応を探します。"),
    (8, 11, "状態フィルターで未対応を選択。"),
    (11, 14, "対応済みの六件を非表示にします。"),
    (14, 17, "未対応の二件だけが残りました。"),
    (17, 20, "このチェック手順を保存して使ってください。"),
)
def phase_at(seconds):
    matches = [i for i, (_, start, end) in enumerate(PHASES) if start <= seconds < end]
    if len(matches) != 1:
        raise ValueError("Outside story timeline")
    return matches[0]
def validate():
    assert PHASES[0][1] == 0 and PHASES[-1][2] == DURATION
    assert all(PHASES[i][2] == PHASES[i+1][1] for i in range(2))
    last = 0
    for start, end, speech in VOICE_SEGMENTS:
        assert start == last and end > start and speech
        last = end
    assert last == DURATION
    return True
PUBLICATION = "NOT_APPROVED"
NARRATION_STATUS = "NOT_VERIFIED"
