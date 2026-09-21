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

    def test_renderer_applies_motion_filter_to_every_scene(self):
        profile = load_profiles()['genres']['ai_productivity']
        beats = profile['beats']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scenes = []
            for index, beat in enumerate(beats):
                image = root / f'{beat}.png'
                audio = root / f'{beat}.wav'
                image.touch()
                audio.touch()
                scenes.append({'index': index, 'beat': beat, 'asset_id': beat, 'visual_kind': profile['visual'][1], 'asset_approved': True, 'audio_approved': True, 'narration': beat, 'caption': beat, 'duration_seconds': 4, 'image_path': image.name, 'audio_path': audio.name})
            manifest = {'schema_version': 1, 'status': 'draft_review_only', 'genre_id': 'ai_productivity', 'scenes': scenes, 'render_ready': False, 'quality_approved': False, 'publish_mode': 'employee_manual_only'}
            path = root / 'manifest.json'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            with patch('genre_video_renderer.subprocess.run') as run:
                render_review_video(path, root, root / 'review.mp4')
            scene_calls = [call.args[0] for call in run.call_args_list if '-vf' in call.args[0]]
            self.assertEqual(len(scene_calls), len(beats))
            for command in scene_calls:
                vf = command[command.index('-vf') + 1]
                self.assertIn('zoompan=', vf)
                self.assertIn('s=1080x1920:fps=30', vf)
                self.assertIn('drawtext=', vf)


if __name__ == '__main__':
    unittest.main()
