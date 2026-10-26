# Single-byte XOR  (`crypto_xor_seed`)

**Family:** crypto_xor  **Difficulty:** easy

## Objective
challenge/cipher.hex contains a short message XORed against a single repeating byte. Recover the plaintext and submit the flag inside it.

Flag format: `FLAG{[a-z0-9_]+}`

## Build / run (Docker)
```bash
docker build --build-arg FLAG='<flag>' -t rle-crypto-xor-seed .
docker run --rm -it rle-crypto-xor-seed       # challenge files land in /challenge/challenge/
```

## Files
| file | role |
|------|------|
| `task.json` | metadata + source-of-truth flag (author/verifier side) |
| `generate.py` | derives the challenge files from `$FLAG` (deterministic) |
| `xorlib.py` | vendored cryptanalysis helpers |
| `solution/solve.py` | reference solution — prints the recovered flag |
| `verifier.py` | `python verifier.py "<flag>"` -> JSON verdict, exit 0/1 |

## Reference approach
See `solution/solve.py`. The author-side harness runs
generate -> solve -> verify end to end:
```bash
python ../../../common/harness.py run . --backend local
```
