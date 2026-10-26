import re
from pathlib import Path
from xorlib import xor

c1 = bytes.fromhex(Path("challenge/c1.hex").read_text().strip())
c2 = bytes.fromhex(Path("challenge/c2.hex").read_text().strip())
known = Path("challenge/known_plaintext.txt").read_bytes()

keystream = xor(c2, known)          # ks = c2 XOR p2
secret = xor(c1, keystream)         # p1 = c1 XOR ks
print(re.search(r"FLAG\{[a-z0-9_]+\}", secret.decode(errors="replace")).group(0))
