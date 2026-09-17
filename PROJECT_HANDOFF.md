# TikTok AI社員システム：チャット間引き継ぎ・開発の唯一の確認起点

最終記録日: 2026-09-18 (JST)。この文書は引き継ぎの索引であり、動画生成の動作保証や全会話の完全な記憶を意味しない。新しいチャットではまず本書を読み、GitHubの最新ブランチ・実行結果・完成動画と照合してから変更すること。更新日以降の情報は再確認すること。

## 最優先のユーザー要件（決定済み）
- 過去の開発で到達した **v33の映像品質を基準**にする。v20を最新完成版として扱わない。ユーザーに旧版テストを繰り返させない。
- 次の品質向上案はComfyUI + Wan 2.2による人物・ロボット・実際の作業画面などの自然な動き。5秒の動画を実生成して確認するまでは完成と記載しない。
- 最終目標: Googleフォームで社員登録・承認 → 社員ごとに企画・台本・高品質な音声付き縦型MP4生成 → 実メディアQA → Google Driveにオリジナル保存 → LINE WORKSで本人へ個別通知 → 本人が確認してTikTokに手動投稿 → 実績・改善データ回収。初期6名、その後100名規模。TikTok自動投稿は現時点で要件に含めない。
- 動画品質の劣化、偽のQA、未実行なのに『完了』と報告することを禁止。ユーザーの承認なく有料GPU契約・外部公開・本番配信をしない。

## 実物から確認した事実（2026-09-18時点）
- リポジトリ: `genokuda0902/tiktok-ai-employee`。
- `main` の `.github/workflows/ai_jitan_complete_video.yml` は v19 Reference Studio。音声、scene plan、motion render、compose、QA、MP4 artifact の手順が記述されている。ワークフローの存在だけでは現在の実行成功は証明できない。
- `main` の `.github/workflows/daily-v2.yml` は毎日 `src/build_daily.py` を実行。これがv33以降の制作系に接続されたことは確認できていない。旧日次ワークフローを完成版と呼ばない。
- PR #5 `feature/employee-qa-real-metrics` は2026-09-18確認時に draft/open/unmerged。説明文に既存 `src/build_daily.py` が `-an` で無音動画を生成する問題が明記されている。**PR #5をマージしない**（v33品質の根拠がない）。
- 以前の isolated v20 workflow run `35241003875` は成功し、`employee-v20-isolated-test-output` artifact（ID `10505103677`）を生成したとの実行履歴がある。これはv20の検証であり、v33の再生成・品質・社員別配布の検証ではない。artifactの保存期限は2026-09-24と記録されている。
- v33の完成動画を過去チャットで評価した履歴はあるが、**v33生成コードの正確なパス・commit・workflow・元MP4の保存先は未特定**。v33がGitHubに保存されているとも、消失したとも断言しない。
- ComfyUI + Wan 2.2の5秒動画について、実生成成功を裏付けるrun/artifactは未確認。過去の会話ではGPU環境が課題とされていたが、現在の環境は再確認が必要。
- Google Forms用 `integrations/google_forms/Code.gs` はPR #5側に保存した履歴があるが、フォームの作成・GAS認可・デプロイは未確認。Drive/LINE WORKS本番接続も未確認。

## 次に実施する作業（順番固定）
1. 過去の「v19 完成確認」「v19 完成確認継続」およびv33/v35開発履歴の**実際のコードパス、commit、run、MP4**を探し、確認できたものだけここに追記する。GitHubのbranch/tag/Actions/artifactと照合。過去チャット全文を自動取得できない場合はその限界を明示し、推測しない。
2. v33を再現する実行コマンド・依存関係・出力・音声・解像度・視覚的品質を実測し、ゴールデンMP4とQA基準を固定する。v20を代用品にしない。
3. ComfyUI + Wan 2.2を実行可能なGPUで5秒試験し、実物を確認。費用が発生する場合はユーザーの承認を得る。
4. 品質を満たす動画制作パイプラインに社員別ジョブ・フォーム承認・QA・Drive・LINE WORKSを接続。権限・秘密情報はGitHub Secrets等で管理し、チャットに貼らせない。
5. 6名で一気通貫の実行ログ・動画・通知・投稿パッケージを検証してから完成と報告。100名化はその後。

## 新しいチャット開始時の手順
このファイルを最初に取得し、`main`と開発ブランチ、PR、最新Actions、成果物を照合する。**『v33は完成動画があった』という会話上の記録と『今、v33を再生成できる』という実証を区別**する。ユーザーに旧テストを再実行させず、ツールでできる確認は自分で行う。変更した場合は本ファイルに日時・commit・テスト結果・次の1手を追記する。チャットをまたいでも自動で全履歴が同期するとは説明しない。

## 参照先
- Repo: https://github.com/genokuda0902/tiktok-ai-employee
- Draft PR #5: https://github.com/genokuda0902/tiktok-ai-employee/pull/5
- v20 isolated run（v33の証拠ではない）: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/35241003875
