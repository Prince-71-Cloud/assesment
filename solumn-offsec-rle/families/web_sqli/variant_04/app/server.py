import os, re
from flask import Flask, request
from appbase import build_db, query

app = Flask(__name__)
db = build_db()

def naive_filter(s: str) -> str:
    # single-pass, case-insensitive removal of keywords (bypassable by nesting)
    return re.sub(r"(?i)(select|union|or)", "", s)

@app.get("/")
def index():
    return "Check if a username is taken: /check?user=alice"

@app.get("/check")
def check():
    user = request.args.get("user", "")
    if " " in user:
        return "blocked: whitespace not allowed", 403
    rows, err = query(
        db, f"SELECT id FROM users WHERE username='{naive_filter(user)}'")
    if err:
        return "User not found"
    return "User found" if rows else "User not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), threaded=True)
