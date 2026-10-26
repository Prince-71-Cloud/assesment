#!/usr/bin/env bash
# Build + solve + verify every task. Default backend is docker; pass "local" to
# run the services/generators as plain subprocesses (no Docker required).
set -euo pipefail
BACKEND="${1:-docker}"
python3 common/harness.py run-all --backend "$BACKEND"
