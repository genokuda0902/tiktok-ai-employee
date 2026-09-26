import unittest
from video_engine.production_v2.drive_persist import private_folder
class DriveChecks(unittest.TestCase):
    def test_private_shared_folder_required(self):
        okay={'mimeType':'application/vnd.google-apps.folder','driveId':'d','capabilities':{'canAddChildren':True},'permissions':[{'type':'user'}]}
        private_folder(okay,'service_account')
        with self.assertRaises(PermissionError):private_folder({**okay,'permissions':[{'type':'anyone'}]},'authorized_user')
        with self.assertRaises(PermissionError):private_folder({**okay,'driveId':None},'service_account')
        with self.assertRaises(PermissionError):private_folder({**okay,'capabilities':{'canAddChildren':False}},'authorized_user')
if __name__=='__main__':unittest.main()
