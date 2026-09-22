import unittest
from unittest.mock import patch
from src.drive_delivery import upload_approved_original, DeliveryBlocked


class Request:
    def __init__(self, fn): self.fn = fn
    def execute(self): return self.fn()


class Files:
    def __init__(self): self.objects = []; self.creates = 0; self.fail_once = False
    def list(self, **kwargs):
        return Request(lambda: {'files': list(self.objects)})
    def create(self, **kwargs):
        def perform():
            self.creates += 1
            obj = dict(kwargs['body'], id='drive-id-1')
            self.objects.append(obj)
            if self.fail_once:
                self.fail_once = False
                raise ConnectionError('response lost after upload')
            return obj
        return Request(perform)


class Service:
    def __init__(self): self.storage = Files()
    def files(self): return self.storage


class DriveTests(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.kwargs = dict(job_id='job-1', account_id='acct-1', folder_id='folder-1',
                           video_bytes=b'fake bytes for adapter test only',
                           qa={'passed': True, 'mock': False}, human_approved=True,
                           rights_approved=True, privacy_approved=True, sleep=lambda _: None)

    def test_qa_rejection_prevents_api_access(self):
        self.kwargs['qa']['passed'] = False
        with self.assertRaises(DeliveryBlocked):
            upload_approved_original(self.service, **self.kwargs)
        self.assertEqual(self.service.storage.creates, 0)

    @patch('googleapiclient.http.MediaIoBaseUpload')
    def test_repeated_upload_returns_same_id(self, media):
        first = upload_approved_original(self.service, **self.kwargs)
        second = upload_approved_original(self.service, **self.kwargs)
        self.assertTrue(first['created'])
        self.assertFalse(second['created'])
        self.assertEqual(first['file_id'], second['file_id'])
        self.assertEqual(self.service.storage.creates, 1)

    @patch('googleapiclient.http.MediaIoBaseUpload')
    def test_lost_response_reconciles_existing_file(self, media):
        self.service.storage.fail_once = True
        result = upload_approved_original(self.service, **self.kwargs)
        self.assertFalse(result['created'])
        self.assertEqual(self.service.storage.creates, 1)


if __name__ == '__main__': unittest.main()
