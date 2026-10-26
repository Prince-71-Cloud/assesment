# Authentication bypass via SQLi  (`web_sqli_v01`)

**Family:** web_sqli  **Difficulty:** easy-medium

## Objective
POST /login builds its WHERE clause from username/password by string concatenation. Log in without valid credentials; the admin page returns the flag.

Flag format: `FLAG{[a-z0-9_]+}`

## Build / run (Docker)
```bash
docker build --build-arg FLAG='<flag>' -t rle-web-sqli-v01 .
docker run --rm -p 8000:8000 rle-web-sqli-v01
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
