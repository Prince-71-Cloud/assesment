import re
from pathlib import Path
from xorlib import xor, best_single_byte, hamming, english_score

ct = bytes.fromhex(Path("challenge/cipher.hex").read_text().strip())

# Step 1: shortlist key lengths by normalised Hamming distance.
def norm_distance(keysize):
    blocks = [ct[i*keysize:(i+1)*keysize] for i in range(6)]
    pairs = [(i, j) for i in range(6) for j in range(i+1, 6)]
    return sum(hamming(blocks[a], blocks[b]) for a, b in pairs) / (len(pairs)*keysize)

candidates = sorted(sorted(range(2, 17), key=norm_distance)[:5])  # shortlist, then prefer smaller

# Step 2: decrypt each candidate and keep the most English-looking plaintext.
# (A multiple of the true key length scores well on Hamming but corrupts case,
#  so the final tie-break is the language score, not the distance.)
best = (float("-inf"), b"")
for keysize in candidates:
    key = bytes(best_single_byte(ct[i::keysize])[0] for i in range(keysize))
    pt = xor(ct, key)
    s = english_score(pt)
    if s > best[0]:
        best = (s, pt)

print(re.search(r"FLAG\{[a-z0-9_]+\}", best[1].decode(errors="replace")).group(0))
