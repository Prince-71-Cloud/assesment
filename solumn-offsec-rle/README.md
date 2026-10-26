# Solumn OffSec RLE — cybersecurity evaluation tasks

Ten offensive-security evaluation tasks for AI models: **2 families × (1 seed +
4 variants)**, each in a Dockerized environment with a reference solution and an
automated verifier, plus a runner that evaluates a model against the suite and a
written review of the results.

| Assignment requirement | Where it lives |
|------------------------|----------------|
| 10 tasks, 2 families, 1 seed + 4 variants each | `families/web_sqli/`, `families/crypto_xor/` |
| Dockerized environment per task | `families/*/*/Dockerfile` (+ `app/` or `generate.py`) |
| Reference solution per task | `families/*/*/solution/solve.py` |
| Automated verifier per task | `families/*/*/verifier.py` (shared impl, per-task `task.json`) |
| Test tasks against an AI model | `model_eval/eval_runner.py` |
| Review the model's outputs | `model_eval/REPORT.md` |

## The two families

- **`web_sqli` — SQL injection.** In-band UNION → auth bypass → schema
  enumeration → blind boolean extraction → blind + filter bypass.
- **`crypto_xor` — XOR / stream-cipher cryptanalysis.** Single-byte → short
  repeating key → longer unknown key → two-time pad → many-time pad.

Each family's `FAMILY.md` explains the gradient and why the variants resist
memorisation (the solution *path* changes, not just a constant).

## Quick start

No Docker needed to validate the logic — the harness has a `local` back-end that
runs each service/generator as a subprocess:

```bash
./run_all.sh local
# -> builds, solves, and verifies all 10 tasks; expects "10/10 tasks passed"
```

With Docker, validate the shipped images end to end:

```bash
./validate_docker.sh        # builds each image, solves it via the docker back-end
```

Run or inspect a single task:

```bash
python3 common/harness.py run families/crypto_xor/variant_03 --backend local
cat families/web_sqli/seed/README.md
```

## Evaluate a model

```bash
# control: reference solvers through the eval path (expect 10/10)
python3 model_eval/eval_runner.py --backend reference

# offline scripted baseline used for REPORT.md (expect 6/10)
python3 model_eval/eval_runner.py --backend mock

# a real model (agentic bash loop, needs a key)
ANTHROPIC_API_KEY=... python3 model_eval/eval_runner.py \
    --backend anthropic --model claude-sonnet-4-6 --max-steps 25
```

Per-task transcripts and a `results.json` are written under
`model_eval/results/<run>/`. The analysis of a baseline run is in
`model_eval/REPORT.md`.

## Repository layout

```
solumn-offsec-rle/
├── README.md                 # this file
├── run_all.sh                # build+solve+verify every task
├── validate_docker.sh        # full Docker reproducibility check
├── common/
│   └── harness.py            # build/solve/verify orchestrator (docker | local)
├── families/
│   ├── web_sqli/   FAMILY.md + seed + variant_01..04
│   └── crypto_xor/ FAMILY.md + seed + variant_01..04
└── model_eval/
    ├── eval_runner.py        # reference | mock | anthropic backends
    └── REPORT.md             # review of a baseline run
```

Every task directory is self-contained:

```
<task>/
├── task.json            # id, type, difficulty, prompt, flag, flag_format
├── Dockerfile           # reproducible environment; flag injected at build time
├── verifier.py          # python verifier.py "<flag>"  -> JSON verdict, exit 0/1
├── solution/solve.py    # reference exploit — prints the recovered flag
├── README.md            # task-facing brief + how to build/run
└── app/ | generate.py   # the vulnerable service, or the challenge generator
```

## Design choices

**One flag, one source of truth.** Each `task.json` holds the flag. Web images
take it as a `--build-arg` and bake it into the database; crypto generators read
it from `$FLAG` and derive the challenge files deterministically. The verifier
reads the same `task.json`, so a flag can never drift out of sync between the
challenge and the grader.

**Variants, not clones.** A variant changes the exploitation path and the flag,
so a model cannot replay a memorised answer across a family — the property that
makes the set useful for training and evaluation rather than just scoring.

**Deterministic, machine-readable grading.** Verifiers emit JSON and an exit
code, tolerate a flag embedded in model prose, and use exact match so an
"almost-right" exploit is scored as a failure.

**Testing note.** All 10 tasks were validated with the `local` back-end in this
environment (Docker-in-Docker was unavailable); the Dockerfiles are provided and
`validate_docker.sh` runs the identical solve/verify loop through real images
wherever Docker is present. See `model_eval/REPORT.md` for the issues found and
fixed during authoring.

## Safety / scope

These are isolated training targets: deliberately-vulnerable toy services and
synthetic ciphertexts, each hiding a synthetic `FLAG{…}` token. Nothing here
targets, scans, or interacts with any real system, and the techniques
(textbook SQLi and XOR cryptanalysis) are standard teaching material used across
public CTF platforms.
