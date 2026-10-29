# cycle970 — Japanese prompt typing demo (REVIEW ONLY)

New improvement versus cycle968: instead of three static explanation cards, scene04 now **types a concrete Japanese instruction** into a visibly labelled **simulation** of an AI prompt editor, followed by a send cue. This more closely follows the user's 16-panel storyboard (panel 4) without falsely presenting a real ChatGPT recording. Only the upper part of frames 261–347 (8.70–11.60s) is replaced; inherited Japanese subtitles and AAC remain in the lower region.

The 10-genre policy palette is shared; only `ai_work` has been reviewed and can render. Other 9 fail closed. This is a reimplementation, not recovered v33 source. Independent ASR and semantic caption alignment are **not verified**. The audio-energy diagnostic is not speech recognition.

Private source MP4 must stay local. Do not upload it, extracted voice, user assets or confidential data to the public repository. Synthetic CI only.

```
python cycle970/typed_prompt.py --source /private/cycle968_PROMPT_CLARITY_JP_REVIEW_ONLY.mp4 --output /private/cycle970_TYPED_PROMPT_JP_REVIEW_ONLY.mp4 --report /private/cycle970_report.json
python -m unittest discover -s cycle970 -p 'test_*.py' -v
ffmpeg -v error -xerror -i /private/cycle970_TYPED_PROMPT_JP_REVIEW_ONLY.mp4 -f null -
```

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, paid API or release without employee approval and rights check.
