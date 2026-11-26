import math
import re
from collections import Counter


def entropy(pw):
    if not pw:
        return 0
    counts = Counter(pw)
    n = len(pw)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def has_sequence(pw):
    pw = pw.lower()
    seqs = ["0123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for s in seqs:
        for i in range(len(s) - 2):
            if s[i:i + 3] in pw:
                return 1
    return 0


def has_repeat(pw):
    return 1 if re.search(r"(.)\1\1", pw) else 0


def extract_features(pw):
    return {
        "length": len(pw),
        "n_upper": sum(c.isupper() for c in pw),
        "n_lower": sum(c.islower() for c in pw),
        "n_digit": sum(c.isdigit() for c in pw),
        "n_symbol": sum(not c.isalnum() for c in pw),
        "n_unique": len(set(pw)),
        "entropy": entropy(pw),
        "has_sequence": has_sequence(pw),
        "has_repeat": has_repeat(pw),
    }