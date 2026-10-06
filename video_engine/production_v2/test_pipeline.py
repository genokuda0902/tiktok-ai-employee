import unittest
from video_engine.production_v2.pipeline import request_revision

class RevisionTests(unittest.TestCase):
    def setUp(self):
        self.plan={'video_id':'v1','version':1,'assets':{'a':{},'b':{}},'scenes':[{'scene_id':1,'asset_id':'a','caption':'old'},{'scene_id':2,'asset_id':'a','caption':'unchanged'}]}
        self.req={'video_id':'v1','requested_by':'trusted-user','requested_at':'2026-09-27T00:00:00Z','scene_id':1,'change_type':'caption','instruction':'Shorten','proposed_value':'new','previous_version':1,'new_version':2,'status':'REQUESTED'}
    def test_only_target_scene_changes_and_version_is_immutable(self):
        revised=request_revision(self.plan,self.req,'trusted-user')
        self.assertEqual(self.plan['scenes'][0]['caption'],'old')
        self.assertEqual(revised['scenes'][0]['caption'],'new')
        self.assertEqual(revised['scenes'][1]['caption'],'unchanged')
        self.assertEqual(revised['version'],2)
    def test_no_self_claimed_identity(self):
        with self.assertRaises(PermissionError): request_revision(self.plan,self.req,None)
        with self.assertRaises(PermissionError): request_revision(self.plan,self.req,'different-user')
    def test_stale_or_arbitrary_changes_rejected(self):
        self.req['new_version']=3
        with self.assertRaises(ValueError): request_revision(self.plan,self.req,'trusted-user')
        self.req['new_version']=2;self.req['change_type']='execute_python'
        with self.assertRaises(ValueError): request_revision(self.plan,self.req,'trusted-user')

if __name__=='__main__':unittest.main()
