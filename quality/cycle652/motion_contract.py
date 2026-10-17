"""Cycle652 reusable 10-genre motion QA contract. No upload or posting code.
All data in the demonstration are synthetic; the contract is fail-closed.
"""
DATA = (120, 150, 200, 180)
GENRES = (
    'AI・仕事効率化', '美容・身だしなみ', '恋愛・心理', 'お金・節約',
    '営業・ビジネス', '転職・キャリア', '健康・生活改善',
    '雑学・科学', '旅行・グルメ', '商品比較・暮らし'
)
SCENES = (
    (0, 2.0, 'AIの合計、検算した？', 'その答え、根拠まで見ていますか？'),
    (2, 4.5, '元データは4つ', 'まず4か月分の数字を確認'),
    (4.5, 7, '指示は具体的に', '集計と計算式、グラフを依頼'),
    (7, 9.5, '4つを足すと？', '順番に足して合計を確認'),
    (9.5, 12, '数式も確認', 'SUM関数で合計を照合'),
    (12, 15, 'グラフでも確認', '棒の高さと数値を一致させる'),
    (15, 17.5, '答えだけ→根拠まで', 'AIの出力は最後に検算'),
    (17.5, 20, '保存して試してみて', 'まずは手元の架空データで練習')
)

def validate_plan():
    assert len(set(GENRES)) == 10
    assert sum(DATA) == 650
    assert len(SCENES) == 8
    assert SCENES[0][0] == 0 and SCENES[-1][1] == 20
    assert all(a[1] == b[0] for a, b in zip(SCENES, SCENES[1:]))
    assert all(1.5 <= end - start <= 3 for start, end, _, _ in SCENES)
    assert all(len(caption) <= 28 for _, _, _, caption in SCENES)
    return True

def display_sum(progress):
    """Never display a misleading intermediate total as the final result."""
    return '650' if progress > 0.72 else '検算中…'

def validate_manifest(m):
    required = {
        'publication': 'NOT_APPROVED',
        'rights': 'UNVERIFIED',
        'japanese_narration': 'ABSENT',
        'caption_sync': 'SCENE_ONLY',
        'posting': 'MANUAL_AFTER_HUMAN_APPROVAL'
    }
    for key, expected in required.items():
        assert m.get(key) == expected, (key, m.get(key))
    assert m.get('genres_supported') == list(GENRES)
    assert m.get('sum') == sum(DATA)
    assert m.get('duration_seconds') == 20
    return True
