# TikTok AI社員 v1

AI時短ラボを1号機として、PCを閉じていてもGitHub Actions上で処理するクラウド型TikTok運営基盤。

## 現在のSTEP
まず GitHub Actions → FFmpeg → 9:16 MP4 → Artifact のクラウド経路を検証する。
このテスト成功後、企画・台本・日本語音声・字幕・QA・2本/日・6アカウント設定を同じ本体へ追加する。

## 固定方針
- Mac/Windowsの常時起動なし
- 追加月額・従量課金APIなし
- TikTokの非公式自動投稿なし
- TikTokパスワード/Cookieを保存しない
- 社員はGitHubを操作しない
