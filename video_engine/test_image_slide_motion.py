import unittest
from image_slide_motion import DEFAULT_EVENTS,MOTION_PROFILES,baked_card_manifest,comparison_filter,end_card_filter,event_manifest_filter,hook_hierarchy_filter,interaction_filter,interactive_motion_filter,motion_filter,semantic_reaction_filter

class ImageSlideMotionTests(unittest.TestCase):
    def test_profiles_are_reusable(self):
        self.assertGreaterEqual(len(MOTION_PROFILES),4)
        for i in range(12):
            value=motion_filter(i); self.assertIn('crop=1080:1920',value); self.assertIn('scale=',value)
    def test_baked_cards_hold_caption_and_comparison_as_image_content(self):
        cards=baked_card_manifest((
            {'role':'hook','headline':'Excel集計、まだ手作業？','caption':'最初の2秒で課題を提示','image':'01.png','duration':2.5},
            {'role':'comparison','headline':'30分 → 3分','caption':'作業時間を90%短縮','image':'06.png','duration':2.5},
            {'role':'cta','headline':'保存してあとで試す','caption':'AI時短の型をストック','image':'08.png','duration':2.5},
        ))
        self.assertEqual(len(cards),3)
        self.assertTrue(all(c['text_baked'] for c in cards))
        self.assertEqual(cards[1]['role'],'comparison')
    def test_baked_cards_fail_closed(self):
        with self.assertRaises(ValueError): baked_card_manifest(())
        with self.assertRaises(ValueError): baked_card_manifest(({'role':'comparison','headline':'x','caption':'','image':'x.png','duration':2},))
        with self.assertRaises(ValueError): baked_card_manifest(({'role':'hook','headline':'x','caption':'y','image':'x.png','duration':2},),720,1280)
    def test_interaction_filter_has_cursor_and_click_pulse(self):
        value=interaction_filter(); self.assertIn('drawbox=',value); self.assertIn('enable=',value)
    def test_event_manifest_uses_explicit_timeline_not_periodic_reaction(self):
        value=event_manifest_filter(DEFAULT_EVENTS); self.assertIn('between(t,0.000,0.560)',value); self.assertIn('between(t,6.500,7.060)',value); self.assertIn('between(t,13.000,13.560)',value); self.assertNotIn('mod(t,2.5)',value); self.assertEqual(value.count('drawbox='),12)
    def test_event_manifest_rejects_invalid_or_unsorted_events(self):
        with self.assertRaises(ValueError): event_manifest_filter(({'start':2,'processing':.5,'result':1.2},{'start':1,'processing':.5,'result':1.2}))
        with self.assertRaises(ValueError): event_manifest_filter(({'start':0,'processing':.8,'result':.4},))
    def test_hook_hierarchy_is_genre_copy_driven(self):
        value=hook_hierarchy_filter('問題提起','便益','/tmp/font.ttc'); self.assertIn('問題提起',value); self.assertIn('便益',value)
    def test_comparison_beat_is_copy_driven_and_timed(self):
        value=comparison_filter('手作業','AIで短縮','/tmp/font.ttc',8,12); self.assertIn('BEFORE',value); self.assertIn('AFTER',value); self.assertIn('between(t,8.000,12.000)',value)
    def test_end_card_is_copy_driven_timed_and_subtle(self):
        value=end_card_filter('保存してあとで試す','/tmp/font.ttc',16.2,19.6); self.assertIn('保存してあとで試す',value); self.assertIn('between(t,16.200,19.600)',value); self.assertIn('sin((t-16.200)*8)',value)
    def test_end_card_fails_closed(self):
        with self.assertRaises(ValueError): end_card_filter('','/tmp/font.ttc')
        with self.assertRaises(ValueError): end_card_filter('保存','/tmp/font.ttc',20,18)
        with self.assertRaises(ValueError): end_card_filter('保存','/tmp/font.ttc',width=720,height=1280)
    def test_semantic_reaction_remains_backward_compatible(self): self.assertIn('mod(t,2.5)',semantic_reaction_filter())
    def test_combined_filter_uses_manifest_reactions(self):
        value=interactive_motion_filter(2); self.assertIn('crop=1080:1920',value); self.assertIn('between(t,6.500,7.060)',value)
    def test_fail_closed_for_non_portrait_target(self):
        with self.assertRaises(ValueError): motion_filter(0,720,1280)
        with self.assertRaises(ValueError): interaction_filter(720,1280)
        with self.assertRaises(ValueError): event_manifest_filter(DEFAULT_EVENTS,720,1280)
        with self.assertRaises(ValueError): hook_hierarchy_filter('問題','便益','/tmp/font.ttc',720,1280)
        with self.assertRaises(ValueError): semantic_reaction_filter(720,1280)
        with self.assertRaises(ValueError): interactive_motion_filter(0,720,1280)

if __name__=='__main__': unittest.main()
