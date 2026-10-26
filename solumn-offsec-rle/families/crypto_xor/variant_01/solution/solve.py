import re
from pathlib import Path
from xorlib import xor, best_single_byte, english_score

ct = bytes.fromhex(Path("challenge/cipher.hex").read_text().strip())

# Try every plausible key length; recover each, keep the most English-looking.
# This beats pure Hamming ranking, which can favour a multiple of the true key.
best = (float("-inf"), b"")
for keysize in range(2, 9):
    key = bytes(best_single_byte(ct[i::keysize])[0] for i in range(keysize))
    pt = xor(ct, key)
    s = english_score(pt)
    if s > best[0]:
        best = (s, pt)

print(re.search(r"FLAG\{[a-z0-9_]+\}", best[1].decode(errors="replace")).group(0))
