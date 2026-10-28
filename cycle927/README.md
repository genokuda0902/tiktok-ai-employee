# cycle927 — review-only human approval gate

Different from cycle925's CTA (#308), cycle926's repeated-task scene (#309), and cycle915's evidence-check UI: this changes **scene 05's publication-status semantics**. Previously green checkboxes in a fictional demonstration could be misread as actual verification. New scene explicitly shows **未承認**, 未確認/確認対象, and **確認完了まで投稿しない**. It never fabricates completion or approval.

- Local MP4: 23.033s H.264, 1080x1920, 30fps, 691 frames, inherited Japanese AAC 48kHz and burned captions.
- 87 frames changed, 11.6–14.5s. Three review states, 10 genre presets. Only ai_work full MP4 generated.
- Source SHA256: 964bf6d21980cd42e6fbe321d51aca66f237df1bd1845c4cfa4da44e0f096c14.
- Local output SHA256: 0693fabe3eb8790d5214da440ffc0dbb12be27f89d4511cb9057fa9fb214ec12.
- Local media QA: full A/V decode PASS, AAC ADTS bitstream identical, scene minimum MAE 21.157, outside scene maximum MAE 1.302, caption/footer maximum MAE 1.066 (quarter resolution), 12/12 technical checks PASS, 8/8 tests PASS.
- GitHub CI checks source, synthetic overlays, and fail-closed policy. **Private MP4 not uploaded to public GitHub**.

## Run (with licensed source media supplied privately)
python cycle927/src/review_gate.py --source SOURCE.mp4 --output REVIEW_ONLY.mp4 --expected-source-sha 964bf6d21980cd42e6fbe321d51aca66f237df1bd1845c4cfa4da44e0f096c14

## Unverified
Independent Japanese ASR and speech/caption meaning/timing, original v33 MP4 direct comparison, inherited media commercial rights, real-device playback, employee approval, actual Actions billing. No merge, auto-post, paid contract, or public media upload. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
