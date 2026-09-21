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

    def test_renderer_applies_typing_processing_result_and_mobile_hook_captions(self):
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
            filters = []
            expected_labels = ('完了', '入力済み', '実行中', '確認済み', '保存済み')
            expected_prompts = ('AIで集計', '表を更新', '要点を抽出', '結果を確認', '内容を保存')
            for index, command in enumerate(scene_calls):
                vf = command[command.index('-vf') + 1]
                filters.append(vf)
                self.assertIn('zoompan=', vf)
                self.assertIn('s=1080x1920:fps=30', vf)
                self.assertIn("drawtext=text='●'", vf)
                self.assertIn("drawtext=text='○'", vf)
                self.assertIn('min(t/1.520,1)', vf)
                self.assertIn("enable='between(t,1.520,1.660)'", vf)
                self.assertIn('x=170:y=1180:w=740:h=120', vf)
                self.assertIn(expected_prompts[index], vf)
                self.assertIn("drawtext=text='▌'", vf)
                self.assertIn("drawtext=text='処理中…'", vf)
                self.assertIn('w=230:h=12', vf)
                self.assertIn("enable='between(t,2.370,2.920)'", vf)
                self.assertIn(f"drawtext=text='{expected_labels[index]}'", vf)
                self.assertIn("enable='gte(t,2.920)'", vf)
                self.assertIn('borderw=3', vf)
                self.assertIn('x=54:y=1450:w=972:h=280', vf)
            first = filters[0]
            self.assertIn('fontsize=72', first)
            self.assertIn("enable='between(t,0,2.2)'", first)
            self.assertIn('x=54:y=180:w=972:h=330', first)
            for later in filters[1:]:
                self.assertNotIn('fontsize=72', later)
            self.assertGreaterEqual(len(set(filters)), 4)


if __name__ == '__main__':
    unittest.main()
