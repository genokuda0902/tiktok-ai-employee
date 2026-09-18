# First post decisions and checkpoint (2026-09-18 JST)

## User-confirmed direction
- Target: first TikTok post for an account aiming at 100,000 followers; goal is not a guarantee of virality.
- v33 original MP4 is the quality reference; six reference videos were uploaded in the ChatGPT session. Do not replace v33 with a primitive slideshow.
- Image-first, but include alternating **human and robot hero images** and cinematic transitions to add visual variation, then actual-looking animated Excel / ChatGPT operation and growing graph. Do not attempt natural robot full-body motion or Wan 2.2.
- Images themselves contain explanatory text, so add **only essential supplementary captions**, never duplicate or obscure existing text. Review on phone-size viewport.
- Confidential images: earlier user explicitly said they must not be published; later user asks why they were omitted. **Do not infer publication permission from that question.** Distinguish visual/reference use from publication use. Require explicit approval for each image and remove or replace all client names, personal data, internal figures and secrets. No confidential assets or original media in GitHub.
- First-post structure: human/robot hook -> recognizable problem -> animated Excel/ChatGPT demo -> animated graph / tangible result -> concise call to action. Preserve narration-to-visual alignment and avoid misleading performance claims.

## Existing files in session (NOT committed to GitHub)
- `/mnt/data/AI_Jitan_v33_REAL_SPREADSHEET.mp4`: uploaded v33 reference.
- `/mnt/data/first_post_v2/build.py`: actual latest first-post generator; SHA256 `b5c0baedd170687a7da6d0731f998bbee96a90c17066f9781d91b2347d423afa`; not yet copied to GitHub, so do not claim code persisted.
- `/mnt/data/first_post_v2/first_post_review.mp4`: actual generated 31.2-second draft; SHA256 `ef84bcbc9f1b25f60fdc1c6a66f4c24951293f495dabe50215d3865a9e40e365`. The script uses v33's old audio and programmatically drawn UI; **no human/robot hero scenes**, not public-ready.
- Do not rely on sandbox files surviving a future session; preserve source in GitHub and safe media in approved durable storage before calling the project recoverable.

## Next actions / release gates
1. Preserve complete build source in GitHub (this checkpoint alone does NOT preserve it), with no private asset bytes and relative configurable input paths.
2. Locate or generate independent, approved human and robot hero visuals; add between UI/demo scenes.
3. Create original script and narration; align screen content and speech. Remove inherited v33 audio from new-topic video.
4. Audit every frame for confidentiality, copyright, readability and false claims. Require explicit user approval for publishable assets.
5. Render and visually inspect the first-post MP4, then commit code/manifest/test report and update PROJECT_HANDOFF.md with exact SHA and reproducible instructions.

Status: direction checkpoint committed; final video and complete source persistence **not completed**.