import os
from flask import Flask, request
from appbase import build_db, query

app = Flask(__name__)
db = build_db()
FLAG = os.environ.get("FLAG", "FLAG{build_arg_not_set}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "POST username & password to /login"
    u = request.values.get("username", "")
    p = request.values.get("password", "")
    rows, err = query(
        db, f"SELECT username FROM users WHERE username='{u}' AND password='{p}'")
    if err:
        return f"Query error: {err}", 500
    if rows:
        return f"Welcome {rows[0][0]}! Admin console flag: {FLAG}"
    return "Invalid credentials", 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), threaded=True)
