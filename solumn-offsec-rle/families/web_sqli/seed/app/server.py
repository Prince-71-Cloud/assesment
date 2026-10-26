import os
from flask import Flask, request
from appbase import build_db, query

app = Flask(__name__)
db = build_db()

@app.get("/")
def index():
    return "Product catalogue. Try /product?id=1"

@app.get("/product")
def product():
    pid = request.args.get("id", "1")
    rows, err = query(db, f"SELECT name, price FROM products WHERE id = {pid}")
    if err:
        return f"Query error: {err}", 500
    if not rows:
        return "No such product"
    return "\n".join(f"{name} - {price}" for name, price in rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), threaded=True)
