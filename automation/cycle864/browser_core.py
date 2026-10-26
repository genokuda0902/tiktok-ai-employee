"""Reusable 10-genre safeguards for local-browser TikTok demonstrations.
No personal data, remote APIs, credentials, or automated posting.
"""
GENRE_ACCENTS = {
    'ai_productivity': '#25D5C0', 'career': '#F6B85E',
    'money': '#76D6A1', 'health': '#86C8F8',
    'learning': '#C5A9F8', 'beauty': '#F5A0C3',
    'travel': '#75C9F6', 'food': '#F5AF77',
    'home': '#A5DB88', 'business': '#7DA9FF',
}
SYNTHETIC_TASKS = ('資料整理', '日報作成', '数値確認', '最終確認')


def accent_for(genre):
    if genre not in GENRE_ACCENTS:
        raise ValueError('unsupported genre')
    return GENRE_ACCENTS[genre]


def compute(done):
    if len(done) != len(SYNTHETIC_TASKS) or any(type(x) is not bool for x in done):
        raise ValueError('exactly four booleans required')
    n = sum(done)
    return {'done': n, 'total': 4, 'pending': 4-n, 'percent': n*25}


def report_text(stats, conclusion_first=False):
    if set(stats) != {'done', 'total', 'pending', 'percent'}:
        raise ValueError('invalid stats keys')
    if stats['total'] != 4 or stats['done'] + stats['pending'] != 4 or stats['percent'] != stats['done']*25:
        raise ValueError('inconsistent stats')
    conclusion = f"今週の進捗は4件中{stats['done']}件完了、達成率{stats['percent']}%です。"
    followup = f"未完了{stats['pending']}件は明日確認します。"
    return '\n'.join((conclusion, followup) if conclusion_first else (followup, conclusion))


def validate_browser_log(log):
    if log.get('synthetic_data') is not True:
        raise ValueError('synthetic-data label missing')
    events = log.get('events', [])
    names = [e['event'] for e in events]
    if names != ['t0', 't1', 't2', 'generate', 'revise']:
        raise ValueError('missing or reordered browser interaction')
    if log['final'] != compute([True, True, True, False]):
        raise ValueError('final browser state does not match computed result')
    if log['final_report'] != report_text(log['final'], conclusion_first=True):
        raise ValueError('final browser report mismatch')
    return True
