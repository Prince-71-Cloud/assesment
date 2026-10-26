# Reproducible environment for crypto_xor_v04.
# The flag is injected at build time so the image is the single source of truth.
FROM python:3.12-slim
WORKDIR /challenge
ARG FLAG="FLAG{build_arg_not_set}"
ENV FLAG=$FLAG
COPY xorlib.py generate.py ./
# Bake the challenge files; the solver/model only ever sees ./challenge.
RUN python generate.py && rm -f generate.py xorlib.py
CMD ["sh", "-c", "echo 'Challenge files are in /challenge/challenge/' && ls -R /challenge/challenge && sleep infinity"]
