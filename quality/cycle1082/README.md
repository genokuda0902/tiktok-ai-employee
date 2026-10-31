# cycle1082 — data-to-chart visual evidence bridge (review only)

Stacked on unmerged cycle1080 Draft PR #482, **not main**. Original reimplementation, not recovered v33 source. New distinct change: scene05 frames 380–428 (12.667–14.300s) turn a verified fictional three-month table into an animated grouped bar chart, then display calculated totals (46+29=75) before scene06's correction example. Earlier scene05 table remains visible until 12.667s.

Dataset is explicitly passed via --data-json, validated, and labelled illustrative. The 10 genre palette presets do not imply completed MP4 tests for all genres. No real-world time-savings or AI accuracy claim.

## Local reproducible commands
\`\`\`bash
python3 -m unittest quality.cycle1082.test_chart_bridge -v
python3 -m quality.cycle1082.chart_bridge --smoke
python3 -m quality.cycle1082.chart_bridge --source /private/cycle1080.mp4 --source-sha VERIFIED_SHA256 --data-json quality/cycle1082/sample_data.json --out /private/cycle1082.mp4 --genre ai_work
\`\`\`

No private MP4, narration, extracted frames, confidential photos or rights-unknown media are committed. CI uses synthetic video and synthetic sine audio only. Existing Japanese narration and 8 burned-in caption sections are inherited; independent speech transcription/meaning and phone playback remain unverified.

Research used accessible summaries of TikTok市場分析/TikTok動画研究 and user's directly inspected 16-panel ChatGPT×Excel storyboard (panels 7–9). Full research transcripts and original v33 MP4 were not accessible. Current 8-scene 23.033s review output remains less cinematic/varied than 16-panel ~36s storyboard. Original robot motion remains out of scope.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, public upload of private footage, auto-post, paid services, or rights assumption.
