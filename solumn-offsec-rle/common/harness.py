#!/usr/bin/env python3
"""
Solumn OffSec RLE — task harness.

One orchestrator for every task in the suite. Given a task directory it will:
  1. BUILD    the challenge environment from a single source-of-truth flag
  2. SOLVE    it with the reference solution (proves the task is solvable)
  3. VERIFY   the recovered flag with the task's automated verifier

Two environment back-ends are supported:
  * docker  — the shipped, reproducible environment (default)
  * local   — run the service / generator as a plain subprocess, no Docker
              (used by CI and by this sandbox, where Docker-in-Docker is absent)

Each task is described by its own task.json; nothing here is task-specific, so
adding a variant means dropping a new directory in, not editing this file.

Usage:
    python common/harness.py run families/web_sqli/seed --backend local
    python common/harness.py run-all --backend local
    python common/harness.py run families/crypto_xor/variant_03
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_task(task_dir: Path) -> dict:
    with open(task_dir / "task.json") as fh:
        return json.load(fh)


def free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_for_port(host: str, port: int, timeout: float = 20.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def run_solution(task_dir: Path, env: dict) -> str:
    """Run solution/solve.py and return its recovered flag (last stdout line)."""
    proc = subprocess.run(
        [sys.executable, str(task_dir / "solution" / "solve.py")],
        cwd=str(task_dir),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"solution failed:\n{proc.stdout}\n{proc.stderr}")
    lines = [l.strip() for l in proc.stdout.splitlines() if l.strip()]
    if not lines:
        raise RuntimeError("solution produced no output")
    return lines[-1]


def run_verifier(task_dir: Path, candidate: str) -> bool:
    proc = subprocess.run(
        [sys.executable, str(task_dir / "verifier.py"), candidate],
        cwd=str(task_dir),
        capture_output=True,
        text=True,
        timeout=30,
    )
    sys.stdout.write(proc.stdout)
    return proc.returncode == 0


# --------------------------------------------------------------------------- #
# back-ends
# --------------------------------------------------------------------------- #
def solve_crypto(task_dir: Path, task: dict) -> str:
    """Generate challenge files from the flag, then run the reference solution."""
    env = dict(os.environ, FLAG=task["flag"])
    subprocess.run(
        [sys.executable, str(task_dir / "generate.py")],
        cwd=str(task_dir), env=env, check=True,
        capture_output=True, text=True,
    )
    return run_solution(task_dir, env)


def solve_web_local(task_dir: Path, task: dict) -> str:
    """Launch the Flask app as a subprocess and run the reference solution.

    The server's stdout/stderr go to a temp FILE, never an unread PIPE: werkzeug
    logs every request, and a blind solver makes hundreds, which would overflow a
    64 KB pipe buffer and deadlock the server mid-run.
    """
    import tempfile

    port = free_port()
    env = dict(os.environ, FLAG=task["flag"], PORT=str(port))
    log = tempfile.TemporaryFile(mode="w+")
    app = subprocess.Popen(
        [sys.executable, str(task_dir / "app" / "server.py")],
        cwd=str(task_dir), env=env, stdout=log, stderr=subprocess.STDOUT,
    )
    try:
        if not wait_for_port("127.0.0.1", port):
            log.seek(0)
            raise RuntimeError(f"service never came up:\n{log.read()}")
        solve_env = dict(env, TARGET=f"http://127.0.0.1:{port}")
        return run_solution(task_dir, solve_env)
    finally:
        app.terminate()
        try:
            app.wait(timeout=5)
        except subprocess.TimeoutExpired:
            app.kill()
        log.close()


def solve_web_docker(task_dir: Path, task: dict) -> str:
    """Build + run the shipped Docker image and run the reference solution."""
    image = f"rle-{task['task_id'].replace('_', '-')}"
    port = free_port()
    subprocess.run(
        ["docker", "build", "--build-arg", f"FLAG={task['flag']}", "-t", image, "."],
        cwd=str(task_dir), check=True,
    )
    cid = subprocess.run(
        ["docker", "run", "-d", "-p", f"{port}:8000", image],
        cwd=str(task_dir), check=True, capture_output=True, text=True,
    ).stdout.strip()
    try:
        if not wait_for_port("127.0.0.1", port):
            raise RuntimeError("container service never came up")
        env = dict(os.environ, TARGET=f"http://127.0.0.1:{port}")
        return run_solution(task_dir, env)
    finally:
        subprocess.run(["docker", "rm", "-f", cid], capture_output=True)


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
def run_one(task_dir: Path, backend: str) -> bool:
    task = load_task(task_dir)
    label = f"{task['task_id']:<24} [{task['difficulty']}]"
    try:
        if task["type"] == "crypto":
            recovered = solve_crypto(task_dir, task)
        elif task["type"] == "web":
            recovered = (solve_web_docker if backend == "docker"
                         else solve_web_local)(task_dir, task)
        else:
            raise RuntimeError(f"unknown task type {task['type']!r}")

        ok = run_verifier(task_dir, recovered)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}  recovered={recovered}")
        return ok
    except Exception as exc:  # noqa: BLE001  (harness surfaces every failure)
        print(f"  ERROR {label}  {exc}")
        return False


def discover() -> list[Path]:
    tasks = []
    for fam in sorted((ROOT / "families").iterdir()):
        for task_dir in sorted(fam.iterdir()):
            if (task_dir / "task.json").exists():
                tasks.append(task_dir)
    return tasks


def main() -> int:
    ap = argparse.ArgumentParser(description="Solumn OffSec RLE harness")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="build+solve+verify one task")
    p_run.add_argument("task_dir")
    p_run.add_argument("--backend", choices=["docker", "local"], default="docker")

    p_all = sub.add_parser("run-all", help="build+solve+verify every task")
    p_all.add_argument("--backend", choices=["docker", "local"], default="docker")

    args = ap.parse_args()

    if args.cmd == "run":
        return 0 if run_one(Path(args.task_dir).resolve(), args.backend) else 1

    tasks = discover()
    print(f"Discovered {len(tasks)} tasks\n")
    results = {str(t.relative_to(ROOT)): run_one(t, args.backend) for t in tasks}
    passed = sum(results.values())
    print(f"\n{passed}/{len(results)} tasks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
