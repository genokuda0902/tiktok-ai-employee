"""Cycle631: generic 10-genre CTA content contract (REVIEW_ONLY)."""
GENRE_STEPS = {
    "ai_productivity": ["範囲 B2:B5 を選択", "=SUM(B2:B5) を入力", "合計 720 を検算"],
    "trivia": ["気になる事実を保存", "一次資料を探す", "条件と日付を確認"],
    "cooking": ["材料を確認", "手順を見直す", "加熱状態を確認"],
    "beauty": ["照明を揃える", "撮影角度を揃える", "加工の有無を確認"],
    "money": ["金額と期間を確認", "計算式を確認", "出典を再確認"],
    "health": ["対象と条件を確認", "信頼できる出典を確認", "個別判断は専門家へ"],
    "travel": ["交通手段を確認", "営業日を確認", "最新料金を確認"],
    "products": ["用途を整理", "仕様を比較", "購入前に価格確認"],
    "story": ["前提を整理", "転換点を確認", "結末の根拠を確認"],
    "work_tips": ["手順を整理", "小さく試す", "結果を確認"],
}
def validate(genre):
    steps = GENRE_STEPS[genre]
    if len(steps) != 3 or any(not s or len(s) > 20 for s in steps):
        raise ValueError("Invalid CTA")
    return tuple(steps)
PUBLICATION = "NOT_APPROVED"
NARRATION = "ABSENT"
