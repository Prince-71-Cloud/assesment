"""Tiny HTTP helper (urllib only, no third-party deps).

Blind extraction fires hundreds of requests, so each call retries briefly on a
transient connection reset rather than aborting the whole solve.
"""
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TARGET = os.environ.get("TARGET", "http://127.0.0.1:8000")


def _open(url: str, data: bytes | None = None, retries: int = 4) -> str:
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, data=data, timeout=15) as r:
                return r.read().decode(errors="replace")
        except urllib.error.HTTPError as e:          # 4xx/5xx carry a body
            return e.read().decode(errors="replace")
        except (urllib.error.URLError, ConnectionError, OSError) as e:
            last = e
            time.sleep(0.1 * (attempt + 1))
    raise last


def get(path: str, **params) -> str:
    qs = urllib.parse.urlencode(params)
    return _open(f"{TARGET}{path}?{qs}" if qs else f"{TARGET}{path}")


def get_raw(path_with_query: str) -> str:
    # Send an already-encoded query string without re-encoding payload syntax.
    return _open(f"{TARGET}{path_with_query}")


def post(path: str, **data) -> str:
    return _open(f"{TARGET}{path}", data=urllib.parse.urlencode(data).encode())
