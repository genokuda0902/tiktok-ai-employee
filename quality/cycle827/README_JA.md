# cycle827 — 音声活動に合わせた字幕タイミング

前回 cycle826 は各場面の字幕3状態を等時間で分割していました。今回は日本語音声から FFmpeg silencedetect で無音区間を検出し、発話している区間の長さと字幕の文字数を用いて表示切替を近似します。8場面・24状態、1080×1920、H.264/AAC 30fps、10ジャンルで再利用できる処理です。

**注意:** ASRや単語単位の強制アラインメントではありません。発音の自然さ・実機表示・参考動画との品質比較は未検証です。社員の目視・聴取確認が必要です。

GitHub Actions は前サイクルのオリジナル画像生成コードを利用し、Open JTalkで日本語音声をオフライン生成します。合成画像には実在アプリ画面・人物写真・個人情報は含みません。Open JTalk nitech_jp_atr503_m001.htsvoice は CC BY 3.0 の帰属情報を要確認。

## 実行
```bash
python -m unittest discover -s quality/cycle827 -p 'test_cycle827.py' -v
python quality/cycle826/cycle826.py --root _cycle827_ci --step slides
python quality/cycle819/make_japanese_fixture819.py --root _cycle827_ci
python quality/cycle827/render827.py --root _cycle827_ci --step render
python quality/cycle827/render827.py --root _cycle827_ci --step verify
```

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**。無断マージ・有料API・自動投稿なし。社員承認後の手動投稿のみ。