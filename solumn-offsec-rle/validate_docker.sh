#!/usr/bin/env bash
# Build each task image and run the reference solver against it through the
# docker back-end. Requires Docker. This is the full reproducibility check for
# the shipped environments.
set -euo pipefail
for d in families/*/*/ ; do
  [ -f "$d/task.json" ] || continue
  echo "== $d =="
  python3 common/harness.py run "$d" --backend docker
done
