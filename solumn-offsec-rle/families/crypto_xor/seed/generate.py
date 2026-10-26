import os
from pathlib import Path
from xorlib import xor

FLAG = os.environ["FLAG"]
KEY = bytes([0x5A])
plaintext = (
    f"Security notice: {FLAG} -- keep this value confidential and "
    f"rotate it at the end of every quarter without exception."
).encode()
Path("challenge").mkdir(exist_ok=True)
Path("challenge/cipher.hex").write_text(xor(plaintext, KEY).hex())
