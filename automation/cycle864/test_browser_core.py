import unittest
from browser_core import (GENRE_ACCENTS, SYNTHETIC_TASKS, accent_for, compute,
                          report_text, validate_browser_log)


class BrowserCoreTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS), 10)
        for key in GENRE_ACCENTS:
            self.assertRegex(accent_for(key), r'^#[0-9A-Fa-f]{6}$')

    def test_unknown_genre(self):
        with self.assertRaises(ValueError): accent_for('unknown')

    def test_synthetic_task_count(self):
        self.assertEqual(len(SYNTHETIC_TASKS), 4)

    def test_zero(self):
        self.assertEqual(compute([False]*4)['percent'], 0)

    def test_three(self):
        self.assertEqual(compute([True,True,True,False]),
                         {'done':3,'total':4,'pending':1,'percent':75})

    def test_full(self):
        self.assertEqual(compute([True]*4)['percent'], 100)

    def test_invalid_length(self):
        with self.assertRaises(ValueError): compute([True])

    def test_invalid_types(self):
        with self.assertRaises(ValueError): compute([1,0,1,0])

    def test_before_after(self):
        s=compute([True,True,True,False]); a=report_text(s); b=report_text(s,True)
        self.assertNotEqual(a,b)
        self.assertTrue(b.startswith('今週の進捗は4件中3件完了、達成率75%です。'))

    def test_inconsistent_stats(self):
        with self.assertRaises(ValueError): report_text({'done':2,'total':4,'pending':1,'percent':50})

    def test_log(self):
        s=compute([True,True,True,False]); log={'synthetic_data':True,'events':[
            {'event':x} for x in ('t0','t1','t2','generate','revise')],
            'final':s,'final_report':report_text(s,True)}
        self.assertTrue(validate_browser_log(log))

    def test_log_rejects_fake_event(self):
        s=compute([True,True,True,False]); log={'synthetic_data':True,'events':[{'event':'fake'}],
            'final':s,'final_report':report_text(s,True)}
        with self.assertRaises(ValueError):validate_browser_log(log)

    def test_log_rejects_unlabeled_data(self):
        with self.assertRaises(ValueError):validate_browser_log({'synthetic_data':False})


if __name__=='__main__':unittest.main()
