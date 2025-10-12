import difflib
from datetime import datetime, timedelta


def check_for_api_key(API_KEY):
    return bool(API_KEY)


def remove_similar_strings(strings, threshold=0.85):
    result = []
    for s in strings:
        if not any(difflib.SequenceMatcher(None, s, r).ratio() > threshold for r in result):
            result.append(s)
    return result


def timestamp_handle(time):
    time = str(time)
    if time.isdigit():
        return int((datetime.now() - timedelta(days=int(time))).timestamp())
    elif time.lower() in ('week', 'month'):
        if time == 'week':
            return int((datetime.now() - timedelta(weeks=1)).timestamp())
        else:
            return int((datetime.now() - timedelta(weeks=4)).timestamp())