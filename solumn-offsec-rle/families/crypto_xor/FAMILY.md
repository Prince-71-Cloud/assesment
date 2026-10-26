# Family: `crypto_xor` — XOR / stream-cipher cryptanalysis

All five tasks attack the same underlying weakness — XOR with a reused or
too-short keystream — along a deliberate difficulty gradient. The shared skill
makes them a *family*; the changing parameters (key, key length, message set,
and flag) make them *variants* a model cannot answer from memory.

| task | difficulty | planted weakness | intended technique |
|------|-----------|------------------|--------------------|
| `seed` | easy | single-byte key | brute-force 256 keys, score by English frequency |
| `variant_01` | easy-medium | short repeating key (3 B) | key-length guess + per-column single-byte solve |
| `variant_02` | medium | longer unknown key (8 B) | Hamming-distance key-length detection, then columns |
| `variant_03` | medium-hard | two-time pad (key reuse) + known plaintext | `ks = c2 ^ p2`, then `p1 = c1 ^ ks` |
| `variant_04` | hard | many-time pad (one keystream, 30 msgs) | per-column maximum-likelihood keystream recovery |

**Why the variants resist memorisation.** The flag differs per task, and each
variant changes the *solution path*, not just a constant: a model that memorised
the seed's single-byte answer still has to detect a key length in `v01`/`v02`,
exploit known-plaintext in `v03`, and run a statistical recovery in `v04`.

**Reproducibility.** Each `generate.py` derives the challenge files
deterministically from `$FLAG` (fixed keys / seeded keystreams), so a rebuild of
the same flag yields byte-identical challenges.
