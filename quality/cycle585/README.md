# cycle585 — 字幕と要点カードの重なりを修復

Baseline: cycle583 MP4。cycle583の要点カードによって字幕の一部が欠けたため、y=1070–1230pxに9区間の専用日本語字幕帯を追加。元AACはbitstream copyで保持。10ジャンルの色設定を共通化。

**注意:** 字幕文言とフレーム境界はcycle581の視覚的な字幕データから再利用。音声認識・自然な日本語かどうか・正確な発話同期は未検証。既存CG素材の権利、スマートフォン実機再生、参考動画との品質同等性も未確認。

コードとテストはこのブランチに保存。完全な再現ZIPには元MP4（GitHub未格納）とQA結果を同梱。
ローカル: `python -m pytest -q tests/test_cycle585.py`; `python build_cycle585.py`; `python qa_cycle585.py`。
依存: Python, Pillow, NumPy, pytest, ffmpeg, Noto CJK font。
予算0円。自動投稿・課金・無断マージなし。**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**。
