import unittest

from video_engine.high_fidelity_delivery_guard import verify_delivery_probe


class HighFidelityDeliveryGuardTests(unittest.TestCase):
    def good_probe(self):
        return {
            "video": {"width": 1080, "height": 1920, "codec_name": "h264", "pix_fmt": "yuv420p", "r_frame_rate": "30/1"},
            "audio": {"codec_name": "aac", "sample_rate": "48000", "channels": 2},
            "duration": 12.8,
        }

    def test_valid_delivery_passes_but_does_not_claim_publish_ready(self):
        result = verify_delivery_probe(self.good_probe())
        self.assertTrue(result["technical_delivery_ok"])
        self.assertTrue(result["human_quality_approval_required"])
        self.assertTrue(result["rights_approval_required"])
        self.assertTrue(result["manual_post_only"])
        self.assertFalse(result["auto_post"])
        self.assertFalse(result["publish_ready_claim_allowed"])
        self.assertTrue(result["zero_cost"])

    def test_wrong_geometry_fails_closed(self):
        probe = self.good_probe()
        probe["video"]["width"] = 720
        with self.assertRaises(ValueError):
            verify_delivery_probe(probe)

    def test_wrong_audio_fails_closed(self):
        probe = self.good_probe()
        probe["audio"]["sample_rate"] = "44100"
        with self.assertRaises(ValueError):
            verify_delivery_probe(probe)

    def test_wrong_codec_or_fps_fails_closed(self):
        probe = self.good_probe()
        probe["video"]["r_frame_rate"] = "24/1"
        with self.assertRaises(ValueError):
            verify_delivery_probe(probe)


if __name__ == "__main__":
    unittest.main()
