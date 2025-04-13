from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DB_FILE = 'database.json'

# Load or initialize database
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    user_id = str(data['user_id'])
    referrer_id = str(data.get('referrer_id', ''))

    db = load_db()
    if user_id not in db:
        db[user_id] = {
            'points': 0,
            'last_mine': datetime.utcnow().isoformat(),
            'referrals': [],
        }
        if referrer_id and referrer_id != user_id:
            if referrer_id in db:
                db[referrer_id]['points'] += 10
                db[referrer_id]['referrals'].append(user_id)
    save_db(db)
    return jsonify({"status": "started"})

@app.route('/mine', methods=['POST'])
def mine():
    user_id = str(request.json['user_id'])
    db = load_db()

    if user_id not in db:
        return jsonify({"error": "User not found"}), 404

    db[user_id]['points'] += 1
    save_db(db)

    return jsonify({"points": db[user_id]['points']})

@app.route('/get_points', methods=['POST'])
def get_points():
    user_id = str(request.json['user_id'])
    db = load_db()
    return jsonify({"points": db.get(user_id, {}).get('points', 0)})

@app.route('/ton_address')
def ton_address():
    return jsonify({"address": "UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH"})

if __name__ == '__main__':
    app.run(debug=True)
