import os
from flask import Flask, request
from appbase import build_db, query

app = Flask(__name__)
db = build_db()

@app.get("/")
def index():
    return "Check if a username is taken: /check?user=alice"

@app.get("/check")
def check():
    user = request.args.get("user", "")
    rows, err = query(db, f"SELECT id FROM users WHERE username='{user}'")
    if err:
        return "User not found"      # errors leak nothing here: truly blind
    return "User found" if rows else "User not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), threaded=True)
