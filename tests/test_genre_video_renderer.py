import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from genre_profiles import load_profiles
from genre_scene_planner import build_scene_manifest
from genre_video_renderer import render_review_video


class RendererTests(unittest.TestCase):
    def test_planner_output_requires_explicit_render_approvals(self):
        profile = load_profiles()['genres']['ai_productivity']
        assets = {beat: {'asset_id': beat, 'approved': True, 'kind': profile['visual'][0]} for beat in profile['beats']}
        manifest = build_scene_manifest('ai_productivity', 'review topic', assets)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'manifest.json'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            with patch('genre_video_renderer.subprocess.run') as run:
                with self.assertRaises(ValueError):
                    render_review_video(path, root, root / 'review.mp4')
                run.assert_not_called()

    def test_renderer_rejects_publishing_state(self):
        profile = load_profiles()['genres']['ai_productivity']
        assets = {beat: {'asset_id': beat, 'approved': True, 'kind': profile['visual'][0]} for beat in profile['beats']}
        manifest = build_scene_manifest('ai_productivity', 'topic', assets)
        manifest['quality_approved'] = True
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'manifest.json'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            with patch('genre_video_renderer.subprocess.run') as run:
                with self.assertRaises(ValueError):
                    render_review_video(path, root, root / 'review.mp4')
                run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
