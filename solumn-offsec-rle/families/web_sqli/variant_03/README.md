# Blind boolean-based SQLi  (`web_sqli_v03`)

**Family:** web_sqli  **Difficulty:** hard

## Objective
GET /check?user=<name> reveals only whether a user exists. No data is echoed. Use the boolean oracle to extract the flag from `secret_flag` one character at a time.

Flag format: `FLAG{[a-z0-9_]+}`

## Build / run (Docker)
```bash
docker build --build-arg FLAG='<flag>' -t rle-web-sqli-v03 .
docker run --rm -p 8000:8000 rle-web-sqli-v03
# then exploit http://localhost:8000
```

## Files
| file | role |
|------|------|
| `task.json` | metadata + source-of-truth flag |
| `app/server.py` | the vulnerable Flask service |
| `app/appbase.py` | shared, deliberately-insecure data layer |
| `solution/solve.py` | reference exploit — prints the recovered flag |
| `verifier.py` | `python verifier.py "<flag>"` -> JSON verdict, exit 0/1 |

## Author-side end-to-end check (no Docker needed)
```bash
python ../../../common/harness.py run . --backend local
```
