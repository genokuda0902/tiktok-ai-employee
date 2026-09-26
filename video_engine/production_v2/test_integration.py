import json
import tempfile
import unittest
from pathlib import Path
from employee_management.core import Registry,Denied
from employee_management.auth import AuthenticatedService
from video_engine.production_v2.integration import Store,load_feedback,METRICS
from video_engine.production_v2.creative import candidates
from video_engine.production_v2.test_fixture import create
from video_engine.production_v2.pipeline import produce

class FixtureVerifier:
    """Explicit test fake; never configure in production."""
    def verify(self,token):
        if token not in ('signed_fixture_admin','signed_fixture_employee'): raise Denied('Invalid token')
        return {'signed_fixture_admin':'100','signed_fixture_employee':'200'}[token]

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.people=Registry(str(self.root/'employees.sqlite'))
        self.people.bootstrap_admin('admin','admin@example.invalid','100')
        self.people.register('employee','employee@example.invalid')
        self.people.decide('admin','employee','approved')
        self.people.bind_identity('employee','200');self.people.db.commit()
        self.s=Store(str(self.root/'system.sqlite'),AuthenticatedService(self.people,FixtureVerifier()))
        self.video='video_e2e_test_0001';self.trace='trace_36261124051_10912516118';self.digest='1da0077100794688c3fc898c1b89dd4680a313c4878d38fcced399400806ed7a'
        self.s.register('signed_fixture_admin',self.video,self.trace,'employee','internal-test',1,self.digest,'17KYfFDppLmPaIbNdrseudG32Z_v8JVG4','QUALITY_NOT_APPROVED','source-artifact-10912516118')
    def test_security_and_duplicate(self):
        with self.assertRaises(Denied):self.s.actor('employee') # self-claimed ID is not authentication
        with self.assertRaises(Denied):self.s.attempt_post_approval('signed_fixture_admin',self.video)
        with self.assertRaises(ValueError):self.s.register('signed_fixture_admin',self.video,self.trace,'employee','internal-test',1,self.digest,'file','QUALITY_NOT_APPROVED','source-artifact-10912516118')
        self.assertEqual(self.s._video(self.video)['posting_state'],'HUMAN_REVIEW')
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM audit WHERE action=?',('approval.denied',)).fetchone()[0],1)
    def test_revision_regeneration_analytics_feedback(self):
        plan_path=create(self.root/'fixture');plan=json.loads(plan_path.read_text());plan['trace_id']=self.trace
        req={'revision_id':'revision-test-001','video_id':self.video,'trace_id':self.trace,'requested_by':'employee','requested_at':'2026-09-27T00:00:00Z','scene_id':1,'change_type':'caption','instruction':'Make scene one caption shorter','proposed_value':'公開禁止・確認用','previous_version':1,'new_version':2,'status':'REQUESTED'}
        with self.assertRaises(Denied):self.s.revision('signed_fixture_admin',plan,req) # not the employee's identity
        revised=self.s.revision('signed_fixture_employee',plan,req)
        self.assertEqual(plan['scenes'][0]['caption'],'連携テスト・公開禁止')
        self.assertEqual(revised['scenes'][1]['caption'],plan['scenes'][1]['caption'])
        plan_path.write_text(json.dumps(revised,ensure_ascii=False))
        produce(plan_path,self.root/'renders')
        dest=self.root/'renders'/f'{self.video}_v2';qa=json.loads((dest/'qa.json').read_text())
        self.s.regenerated('signed_fixture_admin',self.video,req['revision_id'],qa['sha256'],'12U5_yR7uDbtnsYCrNPJY4I6ELnZL0n3z',qa)
        self.assertEqual(self.s._video(self.video)['version'],2)
        with self.assertRaises(Denied):self.s.attempt_post_approval('signed_fixture_admin',self.video)
        blank={k:None for k in METRICS};blank['views']=0
        for variant in ('A','B','C'):self.s.record_metrics('signed_fixture_admin',self.video,variant,'TEST_FIXTURE',blank)
        feedback=self.s.feedback('signed_fixture_employee',self.video)
        self.assertEqual(feedback['data_type'],'TEST_FIXTURE')
        self.assertEqual(feedback['source_metrics'][0]['metrics']['views'],0)
        self.assertIsNone(feedback['source_metrics'][0]['metrics']['likes'])
        loaded=load_feedback(revised,feedback)
        self.assertEqual(len(candidates('AI時短','社会人',self.trace,self.video,feedback)),3)
        self.assertEqual(loaded['prior_feedback']['trace_id'],self.trace)
        (self.root/'e2e_evidence.json').write_text(json.dumps({'video_id':self.video,'trace_id':self.trace,'v1_sha256':self.digest,'v1_drive_file_id':'17KYfFDppLmPaIbNdrseudG32Z_v8JVG4','revision_id':req['revision_id'],'v2_sha256':qa['sha256'],'v2_quality':qa['quality_status'],'v2_drive_file_id':'12U5_yR7uDbtnsYCrNPJY4I6ELnZL0n3z','employee_identity':'TEST_FAKE_ONLY','posting_state':self.s._video(self.video)['posting_state'],'analytics_source':'TEST_FIXTURE','feedback_loaded':True},indent=2))
        print((self.root/'e2e_evidence.json').read_text())

if __name__=='__main__':unittest.main()
