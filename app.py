# app.py
from flask import Flask, render_template, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)

# Load users from file
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

users = load_users()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    data = request.json
    user_id = str(data.get("id"))
    name = data.get("name")
    ref = str(data.get("ref")) if data.get("ref") else None

    if user_id not in users:
        users[user_id] = {
            "name": name,
            "dod": 0,
            "last_mine": time.time(),
            "ref": ref,
            "tasks": {"social": False, "invite": False}
        }
        if ref and ref in users:
            users[ref]["dod"] += 10  # referral bonus
    save_users(users)
    return jsonify(success=True, user=users[user_id])

@app.route("/mine", methods=["POST"])
def mine():
    data = request.json
    user_id = str(data.get("id"))
    user = users.get(user_id)
    if not user:
        return jsonify(success=False)

    now = time.time()
    elapsed = now - user["last_mine"]
    mined = int(elapsed / 2)  # mine 1 DOD every 2 sec
    user["dod"] += mined
    user["last_mine"] = now
    save_users(users)
    return jsonify(success=True, dod=user["dod"])

@app.route("/tasks", methods=["POST"])
def tasks():
    data = request.json
    user_id = str(data.get("id"))
    task_type = data.get("task")
    user = users.get(user_id)
    if not user:
        return jsonify(success=False)

    if not user["tasks"][task_type]:
        user["dod"] += 20
        user["tasks"][task_type] = True
        save_users(users)
    return jsonify(success=True, tasks=user["tasks"], dod=user["dod"])

@app.route("/ton")
def ton():
    return jsonify(address="UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH")

if __name__ == "__main__":
    app.run(debug=True)

