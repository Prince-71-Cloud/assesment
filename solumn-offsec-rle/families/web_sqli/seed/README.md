# In-band UNION-based SQLi  (`web_sqli_seed`)

**Family:** web_sqli  **Difficulty:** easy

## Objective
The product lookup endpoint GET /product?id=<n> is injectable in a numeric context. The flag lives in a separate table `secret_flag`. Use a UNION-based injection to read it.

Flag format: `FLAG{[a-z0-9_]+}`

## Build / run (Docker)
```bash
docker build --build-arg FLAG='<flag>' -t rle-web-sqli-seed .
docker run --rm -p 8000:8000 rle-web-sqli-seed
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
