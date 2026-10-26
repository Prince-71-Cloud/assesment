import os
from pathlib import Path
from xorlib import xor

FLAG = os.environ["FLAG"]
KEY = b"Zap"
plaintext = (
    "To whoever is reading this transmission: the operations team has rotated "
    f"the master credential. The new recovery flag is {FLAG} and it must be "
    "stored only inside the hardware vault, never in plaintext configuration."
).encode()
Path("challenge").mkdir(exist_ok=True)
Path("challenge/cipher.hex").write_text(xor(plaintext, KEY).hex())
