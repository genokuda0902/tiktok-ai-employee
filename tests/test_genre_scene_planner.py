import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from genre_profiles import load_profiles
from genre_scene_planner import build_scene_manifest


class GenreScenePlannerTests(unittest.TestCase):
    def test_all_ten_genres_generate_review_only_manifest(self):
        for genre_id, profile in load_profiles()['genres'].items():
            with self.subTest(genre=genre_id):
                assets = {beat: {'asset_id': f'approved-{i}', 'approved': True, 'kind': profile['visual'][0]} for i, beat in enumerate(profile['beats'])}
                result = build_scene_manifest(genre_id, 'sample topic', assets)
                self.assertEqual(len(result['scenes']), len(profile['beats']))
                self.assertFalse(result['render_ready'])
                self.assertFalse(result['quality_approved'])
                self.assertEqual(result['publish_mode'], 'employee_manual_only')
                self.assertTrue(all(scene['narration'] is None for scene in result['scenes']))

    def test_missing_approval_blocks(self):
        profile = load_profiles()['genres']['ai_productivity']
        assets = {beat: {'asset_id': beat, 'approved': True, 'kind': profile['visual'][0]} for beat in profile['beats']}
        assets[profile['beats'][0]]['approved'] = False
        with self.assertRaises(ValueError):
            build_scene_manifest('ai_productivity', 'topic', assets)

    def test_unapproved_visual_kind_blocks(self):
        profile = load_profiles()['genres']['ai_productivity']
        assets = {beat: {'asset_id': beat, 'approved': True, 'kind': profile['visual'][0]} for beat in profile['beats']}
        assets[profile['beats'][0]]['kind'] = 'unknown_private_video'
        with self.assertRaises(ValueError):
            build_scene_manifest('ai_productivity', 'topic', assets)

    def test_unknown_genre_blocks(self):
        with self.assertRaises(ValueError):
            build_scene_manifest('unknown', 'topic', {})

    def test_empty_topic_blocks(self):
        with self.assertRaises(ValueError):
            build_scene_manifest('ai_productivity', ' ', {})


if __name__ == '__main__':
    unittest.main()
