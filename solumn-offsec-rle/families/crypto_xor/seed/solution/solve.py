import re
from pathlib import Path
from xorlib import best_single_byte

ct = bytes.fromhex(Path("challenge/cipher.hex").read_text().strip())
_, _, pt = best_single_byte(ct)
print(re.search(r"FLAG\{[a-z0-9_]+\}", pt.decode(errors="replace")).group(0))
