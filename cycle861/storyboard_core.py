"""Cycle861 reusable 10-genre storyboard contract; standard library only."""
from dataclasses import dataclass
from typing import Tuple

GENRE_ACCENTS = {
    'ai_productivity': '#37E0CC', 'career': '#F2B75E', 'money': '#66D7B0',
    'health': '#8BC4FF', 'learning': '#C4A7FF', 'beauty': '#F79DC2',
    'travel': '#7ED5F0', 'food': '#FFAE7E', 'home': '#B5DB8B', 'business': '#73A8FF',
}
FRAME_BOUNDARIES = (0, 99, 177, 255, 342, 429, 519, 597, 691)
FPS = 30
WIDTH, HEIGHT = 1080, 1920
SUBTITLE_BOX = (70, 1260, 1010, 1480)
SAFE_CONTENT_BOTTOM = 1550

@dataclass(frozen=True)
class Scene:
    title: Tuple[str, ...]
    step: str
    kicker: str
    card_title: str
    card_lines: Tuple[str, ...]
    photo: str
    kind: str = 'photo'

SCENES = (
    Scene(('AIで仕事を', 'もっと早く。'), '01', 'START', '今日から試せる3つの準備', ('作業を選ぶ  →  見本を用意', '→  AIに伝える'), 'photo_01.png'),
    Scene(('繰り返す作業を', '書き出す'), '02', 'FIND', 'まずは1つだけ選ぶ', ('毎朝の定型メール', '同じ形式の日報', '週次の数字まとめ'), 'photo_02.png'),
    Scene(('完成形の見本を', '先に用意'), '03', 'EXAMPLE', '完成イメージを3行で', ('件名：今週の進捗共有', '本文：結論 → 数字 → 次の行動', '文体：丁寧・簡潔'), 'photo_05.png'),
    Scene(('目的と条件を', '具体的に'), '04', 'PROMPT', '入力する指示の例', ('目的：進捗を共有する', '相手：社内メンバー', '条件：丁寧・150字以内'), 'photo_04.png'),
    Scene(('AIの出力は', '人が確認'), '05', 'REVIEW', '生成文の例（架空）', ('「今週の進捗をご報告します。', '予定との差分を確認し、', '次の対応を共有します。」'), 'photo_03.png'),
    Scene(('修正は', '1つずつ伝える'), '06', 'REFINE', '修正依頼の例', ('「結論を先頭に移動して」', '→  変更点を絞って再生成'), 'vector_review.png', 'vector'),
    Scene(('使える指示を', 'テンプレ保存'), '07', 'SAVE', '再利用する型', ('目的：[共有する内容]', '相手：[読む人]', '条件：[長さ・文体]'), 'photo_07.png'),
    Scene(('小さな時短を', '毎日の習慣に'), '08', 'REPEAT', 'まずは明日も1回', ('□  同じ作業に使う', '□  出力を確認する', '□  良い指示を残す'), 'vector_habit.png', 'vector'),
)

def validate_contract(beats):
    assert len(GENRE_ACCENTS) == 10
    assert len(SCENES) == 8
    assert len(FRAME_BOUNDARIES) == 9
    assert FRAME_BOUNDARIES[0] == 0 and FRAME_BOUNDARIES[-1] == 691
    assert all(b > a for a,b in zip(FRAME_BOUNDARIES,FRAME_BOUNDARIES[1:]))
    assert SUBTITLE_BOX[3] < SAFE_CONTENT_BOTTOM
    assert len(beats) == 24
    assert all(0 <= b['start'] < b['end'] <= FRAME_BOUNDARIES[-1]/FPS + 0.001 for b in beats)
    assert all(a['end'] <= b['start'] for a,b in zip(beats, beats[1:]))
    assert all(len(s.card_lines) <= 3 and len(s.title) == 2 for s in SCENES)
    return True
