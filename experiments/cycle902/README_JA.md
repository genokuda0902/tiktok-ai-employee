# cycle902 — 3段階のタスク選択ストーリーボード（レビュー専用）

前回cycle900の「AI出力の人間確認パネル」、並行cycle901の「暫定値のラベル」とは異なり、第2場面（2.9–5.8秒）の一覧表示を、洗い出す→繰り返しを選ぶ→最初の1つを決める、という視覚的な3段階に置換。架空例のみ。実績や効果を保証しない。

- 画像スライド：Pillow / Noto CJK でネイティブ解像度の3段階パネルを描画。
- 既存の日本語音声・焼込字幕を維持し、字幕開始位置 y1450 より上だけを変更。
- 10ジャンルの例示テキストはホワイトリスト。動画実生成はAI仕事効率化ジャンル1本のみ。
- ローカル実行：python experiments/cycle902/task_storyboard.py overlays --genre ai
- ローカル映像合成：bash experiments/cycle902/render.sh PRIVATE_SOURCE.mp4 PRIVATE_OUTPUT.mp4 overlays
- テスト：python -m unittest discover -s experiments/cycle902 -p 'test_*.py' -v （Pillowが必要）。
- 元映像・音声・完成MP4はGitHubにアップロードしない。GitHubにはコードとテストのみ。
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED。素材利用権、独立日本語ASR、スマートフォン再生、v33原本比較、社員承認は未検証。課金・マージ・自動投稿は禁止。
