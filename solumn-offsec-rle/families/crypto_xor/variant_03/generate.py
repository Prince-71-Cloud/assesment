import os, hashlib
from pathlib import Path
from xorlib import xor

FLAG = os.environ["FLAG"]
secret = (
    f"Internal memo: the recovery flag is {FLAG}. Do not share it outside the "
    "security team under any circumstances whatsoever."
).encode()
known = (
    "Welcome to the Acme Corp employee portal. Please authenticate using your "
    "single sign-on credentials before the session timer below reaches zero."
).encode()
# deterministic keystream, at least as long as both messages
ks = hashlib.sha256(b"two-time-pad-seed").digest()
while len(ks) < max(len(secret), len(known)):
    ks += hashlib.sha256(ks).digest()
Path("challenge").mkdir(exist_ok=True)
Path("challenge/c1.hex").write_text(xor(secret, ks).hex())
Path("challenge/c2.hex").write_text(xor(known, ks).hex())
Path("challenge/known_plaintext.txt").write_bytes(known)
