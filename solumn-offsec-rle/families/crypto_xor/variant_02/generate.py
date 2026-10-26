import os
from pathlib import Path
from xorlib import xor

FLAG = os.environ["FLAG"]
KEY = b"Th3_K3y!"
plaintext = (
    "Field report, encrypted channel. Visibility on the perimeter sensors "
    "remains nominal and no intrusions were logged during the overnight "
    f"window. Archive the following recovery flag with the auditors: {FLAG}. "
    "Remember that reusing a short key over a long message exposes the key "
    "length through repeated-block statistics, which is exactly how this "
    "ciphertext will be recovered by anyone who intercepts it in transit."
).encode()
Path("challenge").mkdir(exist_ok=True)
Path("challenge/cipher.hex").write_text(xor(plaintext, KEY).hex())
