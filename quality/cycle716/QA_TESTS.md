# QA test plan

1. Eight scenes span 24 seconds, 3 seconds each.
2. Caption bounding box x75 y1575 w930 h140; right edge 1005, bottom edge 1715.
3. Platform safe bottom begins y1720.
4. MP4 must have H264 1080x1920 30fps, AAC BGM only.
5. Never mark narration as present without a Japanese voice track.
6. Verify full media decode and compare frame 13.5s with cycle715.
