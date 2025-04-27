import difflib

def remove_similar_strings(strings, threshold=0.85):
    result = []
    for s in strings:
        if not any(difflib.SequenceMatcher(None, s, r).ratio() > threshold for r in result):
            result.append(s)
    return result