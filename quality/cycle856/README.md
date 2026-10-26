# cycle856 – six independent high-resolution AI photo sources (review only)

Stacked on unmerged cycle855 PR #199. This cycle replaces six of eight low-resolution photo sources with six independently generated 941x1672 / 1024x1536 AI images, keeping two inherited photos. The foreground photo stage increases from 630x420 to 630x630 pixels (+50% area), and all eight sources are crop-fitted without sharp-image upscaling.

The GitHub files here implement and test the reusable ten-genre photo geometry and no-upscale guard. The local review ZIP contains the **full** 1080x1920 slide generator, inherited Japanese audio, subtitle manifest, MP4 renderer, images, 691-frame finished video, and 16-point QA report. CI **does not** reproduce the finished MP4.

The generated images depict fictional people. Human review of generated visual artifacts, rights/provenance, Japanese pronunciation, forced subtitle alignment, phone playback and employee publication approval remains pending.

No merge, paid service, or posting. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
