import re, json
from pathlib import Path
from xorlib import xor, english_score

cts = [bytes.fromhex(h) for h in json.loads(Path("challenge/ciphertexts.json").read_text())]
maxlen = max(len(c) for c in cts)

# Per-column maximum likelihood: with many messages sharing one keystream, the
# key byte for a column is the one that makes the whole column look most like
# English. Score every candidate key byte against all samples in the column and
# keep the best. More discriminating than binary space-detection.
keystream = bytearray(maxlen)
for p in range(maxlen):
    col = bytes(c[p] for c in cts if p < len(c))
    keystream[p] = max(range(256), key=lambda k: english_score(xor(col, bytes([k]))))

# The flag format is known, so use it to pick the right message.
for c in cts:
    pt = xor(c, bytes(keystream)).decode(errors="replace")
    m = re.search(r"FLAG\{[a-z0-9_]+\}", pt)
    if m:
        print(m.group(0))
        break
