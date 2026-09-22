import tempfile
import unittest
from pathlib import Path
from src.automation_pipeline import select_plan, mock_renderer, process, safe_handoff


def plan():
    return {'run_id':'r1','account_id':'a1','plan_id':'p1','topic':'AI','script':'Original script','generation_settings':{},'approved':True,'script_approved':True,'assets_approved':True,'priority':1}


class PipelineTests(unittest.TestCase):
    def test_approved_selection(self):
        self.assertEqual(select_plan([plan()])['plan_id'], 'p1')
        with self.assertRaises(ValueError):
            select_plan([{**plan(), 'assets_approved':False}])

    def test_mock_never_success(self):
        self.assertIsNone(mock_renderer(plan())['video_path'])
        with tempfile.TemporaryDirectory() as tmp:
            events=[]
            result=process([plan()],str(Path(tmp)/'db.sqlite'),renderer=mock_renderer,notifier=events.append)
            self.assertEqual(result['status'],'renderer_not_connected')
            self.assertEqual(events[0]['event'],'renderer_not_connected')
            self.assertEqual(process([plan()],str(Path(tmp)/'db.sqlite'))['status'],'duplicate_rejected')

    def test_qa_rejection_not_delivered(self):
        with tempfile.TemporaryDirectory() as tmp:
            events=[]
            result=process([plan()],str(Path(tmp)/'db.sqlite'),renderer=lambda _: {'video_path':'/missing.mp4'},notifier=events.append)
            self.assertEqual(result['status'],'qa_failed')
            self.assertEqual(events[0]['event'],'qa_failed')
            with self.assertRaises(PermissionError):
                safe_handoff(plan(),'/missing.mp4',{'passed':False},Path(tmp)/'handoff',human_approved=True,rights_approved=True)
            self.assertFalse((Path(tmp)/'handoff').exists())

    def test_no_unapproved_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(PermissionError):
                safe_handoff(plan(),'/missing.mp4',{'passed':True,'human_visual_privacy_approval':False},Path(tmp)/'handoff',human_approved=True,rights_approved=True)


if __name__=='__main__':
    unittest.main()
