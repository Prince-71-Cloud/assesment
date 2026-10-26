"""Minimal XOR / cryptanalysis helpers, vendored so each task is self-contained."""
from itertools import cycle


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ k for b, k in zip(data, cycle(key)))


# Relative English letter frequencies (plus space), used to score candidate
# plaintexts.  Higher score = more English-looking.
_FREQ = {
    " ": 13.0, "e": 12.7, "t": 9.1, "a": 8.2, "o": 7.5, "i": 7.0, "n": 6.7,
    "s": 6.3, "h": 6.1, "r": 6.0, "d": 4.3, "l": 4.0, "u": 2.8, "c": 2.8,
    "m": 2.4, "w": 2.4, "f": 2.2, "g": 2.0, "y": 2.0, "p": 1.9, "b": 1.5,
}


def english_score(data: bytes) -> float:
    # Case-sensitive on purpose: a multiple of the true key length decrypts to
    # the right letters with the wrong CASE, so rewarding lowercase lets the
    # true key length win the tie-break instead of its multiple.
    score = 0.0
    for byte in data:
        if byte == 0x20:                       # space: very common
            score += 13.0
        elif 97 <= byte <= 122:                # lowercase: reward by frequency
            score += _FREQ.get(chr(byte), 0.5)
        elif 65 <= byte <= 90:                 # uppercase: allowed, barely rewarded
            score += 0.2
        elif 32 <= byte < 127 or byte in (9, 10, 13):
            score += 0.1                        # other printable
        else:
            score -= 8.0                        # non-printable: strong penalty
    return score


def best_single_byte(block: bytes):
    """Return (key_byte, score, plaintext) for the best single-byte XOR key."""
    best = (0, float("-inf"), b"")
    for k in range(256):
        pt = xor(block, bytes([k]))
        s = english_score(pt)
        if s > best[1]:
            best = (k, s, pt)
    return best


def hamming(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))
