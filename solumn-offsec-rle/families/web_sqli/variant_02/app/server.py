import os, secrets
from flask import Flask, request
from appbase import build_db, query

SECRET_TABLE = "t_" + secrets.token_hex(4)
app = Flask(__name__)
db = build_db(secret_table=SECRET_TABLE)

@app.get("/")
def index():
    return "Search the catalogue: /search?q=Key"

@app.get("/search")
def search():
    term = request.args.get("q", "")
    rows, err = query(
        db, f"SELECT name, price FROM products WHERE name LIKE '%{term}%'")
    if err:
        return f"Query error: {err}", 500
    if not rows:
        return "No matches"
    return "\n".join(f"{a} - {b}" for a, b in rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), threaded=True)
