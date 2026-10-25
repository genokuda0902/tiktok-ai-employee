# cycle831 — 写真主体の日本語TikTok画像スライド（レビュー専用）

## 差分
- 既存の図解・架空PC画面中心の8枚を、写真主体のエディトリアルな縦型レイアウトへ変更。
- 字幕を画面中央下の専用領域に移動（ASS pos(540,1640)）し、ラベルとの重なりを回避。
- 日本語音声（cycle828のオフライン音声）・24状態の日本語字幕・1080×1920 / 30fps / 775フレームを維持。
- 10ジャンル配色の回帰テストと、実際に映像が変わったかのCI比較ゲートを追加。

## 素材・再現性の重要な違い
ローカルMP4では、このチャットで新規生成した8コマのAI画像から写真部分を抽出して使用。**AI画像の元データはこのPRにコミットしていない**ため、CIは既存のオリジナルPillow図解を代替素材として使用する。同じ構成コードだが、ローカル版とCI版の映像一致は主張しない。AI画像は合成人物であり、実在人物の同定や利用者の個人情報は含めない。

## 実行
1. python quality/cycle826/cycle826.py --root _review --step slides
2. python quality/cycle819/make_japanese_fixture819.py --root _review
3. python quality/cycle828/render828.py --root _review --step render
4. python quality/cycle831/scene831.py --root _review --step slides （CI用代替画像）
5. python quality/cycle831/scene831.py --root _review --step render
6. python quality/cycle831/scene831.py --root _review --step verify

実際のAI画像を使う場合は手順4で --collage /path/to/approved_storyboard.png を指定。公開権利の最終確認前に自動公開しないこと。

## 未検証
日本語の発音・意味の正確さ、単語単位字幕同期、スマホ実機でのUI干渉、素材・音声モデルの公開権利、参考動画との同等品質、社員承認、Actionsの請求額。

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**。社員承認後の手動投稿のみ。自動投稿、無断マージ、課金操作は禁止。
