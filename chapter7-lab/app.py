"""stockroom-api -- Chapter 7 lab service.

WARNING: this file is DELIBERATELY VULNERABLE. It exists so CodeQL has real
findings to report in Lab 2. Never copy the LAB-VULN patterns into real code.
"""
import os
import re
import sqlite3
import subprocess
from contextlib import closing

from flask import Flask, jsonify, request, send_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

app = Flask(__name__)
app.config["DB_PATH"] = os.environ.get(
    "LAB_DB_PATH", os.path.join(BASE_DIR, "inventory.db")
)

SEED_ITEMS = [("pallet-jack", 4), ("rfid-reader", 12), ("label-printer", 3)]


def init_db():
    with closing(sqlite3.connect(app.config["DB_PATH"])) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS items "
            "(id INTEGER PRIMARY KEY, name TEXT UNIQUE, qty INTEGER)"
        )
        conn.executemany(
            "INSERT OR IGNORE INTO items (name, qty) VALUES (?, ?)", SEED_ITEMS
        )
        conn.commit()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/items")
def items():
    name = request.args.get("name", "")
    with closing(sqlite3.connect(app.config["DB_PATH"])) as conn:
        # LAB-VULN-1 (SQL injection): user input is formatted into the query.
        rows = conn.execute(
            f"SELECT id, name, qty FROM items WHERE name = '{name}'"
        ).fetchall()
    return jsonify([{"id": r[0], "name": r[1], "qty": r[2]} for r in rows])


@app.get("/reports")
def reports():
    filename = request.args.get("file", "daily.txt")
    # LAB-VULN-2 (path traversal): user input is joined into a file path.
    return send_file(os.path.join(REPORTS_DIR, filename))


@app.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    if not re.fullmatch(r"[A-Za-z0-9\.\-:]+", host):
        return jsonify(error="invalid host"), 400
    result = subprocess.run(
        ["ping", "-c", "1", host], capture_output=True, text=True
    )
    return jsonify(host=host, returncode=result.returncode)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
