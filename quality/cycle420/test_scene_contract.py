import unittest
from scene_contract import Scene, validate, verify_voice, ContractError

SCENES=[Scene(str(i), 'caption', 'voice', 2.5) for i in range(8)]

class TestSceneContract(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(SCENES, rights='ORIGINAL_PROCEDURAL', publication='NOT_APPROVED'))
    def test_unknown_rights(self):
        with self.assertRaises(ContractError):
            validate(SCENES, rights='UNKNOWN', publication='NOT_APPROVED')
    def test_voice_provenance(self):
        with self.assertRaises(ContractError):
            verify_voice([1.0]*8, engine='UNKNOWN', segments=SCENES)
