# Reproducible environment for web_sqli_v02.
FROM python:3.12-slim
WORKDIR /app
ARG FLAG="FLAG{build_arg_not_set}"
ENV FLAG=$FLAG
ENV PORT=8000
RUN pip install --no-cache-dir flask==3.0.3
COPY app/ ./
EXPOSE 8000
CMD ["python", "server.py"]
