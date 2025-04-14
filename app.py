sk me, [4/13/2025 8:59 PM]
import os
import time
import random
import string
from flask import Flask, request, render_template_string, jsonify

app = Flask(name)

# ---------------------------
# In-memory storage for user accounts (for demonstration only).
# In production, use a persistent database.
# ---------------------------
user_data = {}  # key: user_id; value: dict with 'name', 'referral_code', 'balance', and 'referred_by'

def generate_referral_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# ---------------------------
# Frontend Template (HTML, CSS, JavaScript)
#
# This sample app uses query parameters to simulate Telegram Web App init data.
# It includes a button to “Send Real TON Transaction”. When clicked, the app will
# use TON Connect SDK to allow the user to connect their wallet and send a transaction
# to the recipient address: UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH.
# ---------------------------
frontend_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DOD Mining App</title>
  <!-- Telegram Web App JS -->
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <!-- Include TON Connect SDK from CDN -->
  <script src="https://unpkg.com/@tonconnect/sdk@0.2.16/dist/tonconnect.umd.js"></script>
  <style>
    body {
      margin: 0;
      padding: 20px;
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      color: #333;
    }
    header {
      text-align: center;
      margin-bottom: 20px;
    }
    header img {
      max-height: 60px;
      vertical-align: middle;
      margin-right: 10px;
    }
    h1 {
      display: inline-block;
      vertical-align: middle;
      font-size: 2em;
      margin: 0;
    }
    .info {
      margin-bottom: 20px;
      font-size: 1.1em;
    }
    .buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin-bottom: 20px;
    }
    .buttons button {
      padding: 10px 20px;
      font-size: 1em;
      border: none;
      border-radius: 5px;
      background-color: #007bff;
      color: white;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .buttons button:hover {
      background-color: #0056b3;
    }
    .output {
      text-align: center;
      font-size: 1.2em;
      padding: 10px;
      background: #ddd;
      border-radius: 5px;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <header>
    <!-- You can replace this with your own logo URL or an embedded Base64 image -->
    <img src="https://via.placeholder.com/60?text=Logo" alt="Logo">
    <h1>DOD Mining App</h1>
  </header>
  <div class="info">
    <p>Welcome, <strong id="username"></strong>!</p>
    <p>Your referral code: <span id="ref-code">N/A</span></p>
    <p>Your balance: <span id="balance">0</span> DOD</p>
    <p id="referred-info"></p>
  </div>
  <div class="buttons">
    <button onclick="sendAction('upgrade')">Upgrade Mining</button>
    <button onclick="sendAction('tap')">Tap Mining</button>
    <button onclick="sendAction('spin')">Spin & Earn</button>
    <button onclick="sendAction('airdrop')">Airdrop</button>
    <button onclick="sendAction('generate_referral')">Generate Referral Link</button>
    <button onclick="sendRealTonTransaction()">Send TON Transaction</button>
  </div>
  <div class="output" id="output">Status messages will appear here</div>
  
  <script>
    // Parse query parameters (simulate Telegram Web App init data)
    const params = new URLSearchParams(window.location.search);
    const userId = params.get('user_id') || 'unknown';
    const userName = params.get('name') || 'Guest';
    const referralFrom = params.get('ref') || null;

sk me, [4/13/2025 8:59 PM]
// Display user name
    document.getElementById('username').innerText = userName;
    
    // User object to be sent to the backend
    const user = { user_id: userId, name: userName };
    
    // Function to send action request to our backend endpoints
    function sendAction(action) {
      fetch('/' + action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById('output').innerText = data.message;
        if (data.balance !== undefined) {
          document.getElementById('balance').innerText = data.balance;
        }
        if (data.referral_code) {
          document.getElementById('ref-code').innerText = data.referral_code;
        }
      })
      .catch(err => {
        document.getElementById('output').innerText = 'Error: ' + err;
      });
    }
    
    // Function to connect TON wallet and send a real transaction
    async function sendRealTonTransaction() {
      try {
        // Create an instance of TonConnect
        const tonconnect = new TonConnect.TonConnect({ manifestUrl: window.location.origin + '/ton-manifest.json' });
        // Connect the user's TON wallet
        const wallet = await tonconnect.connect();
        console.log("Wallet connected:", wallet);
        // Build transaction parameters
        // Note: TON uses nanoton (1 TON = 10^9 nanoton). Adjust the amount as needed.
        const tx = {
          to: "UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH",
          value: "1000000000", // 1 TON (in nanoton)
          bounce: true,
          payload: ""
        };
        // Send the transaction via the wallet
        const result = await wallet.sendTransaction(tx);
        alert("Transaction sent! TX Hash: " + result);
        document.getElementById('output').innerText = "TON transaction sent. TX Hash: " + result;
      } catch (error) {
        console.error("Error sending transaction:", error);
        alert("Transaction failed: " + error.message);
        document.getElementById('output').innerText = "TON transaction failed: " + error.message;
      }
    }
    
    // On page load, inform the backend about the user (and referral if applicable)
    window.addEventListener('load', () => {
      fetch('/init_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          name: userName,
          ref: referralFrom
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.referral_code) {
          document.getElementById('ref-code').innerText = data.referral_code;
        }
        document.getElementById('balance').innerText = data.balance;
        if (data.referred_by) {
          document.getElementById('referred-info').innerText = "Referred by: " + data.referred_by;
        }
        document.getElementById('output').innerText = data.message;
      })
      .catch(err => {
        document.getElementById('output').innerText = 'Error initializing user';
      });
    });
  </script>
</body>
</html>
"""

# ---------------------------
# Backend Routes
# ---------------------------

# Initialize user account and handle referrals.
@app.route('/init_user', methods=['POST'])
def init_user():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name', 'Guest')
    ref = data.get('ref')
    
    if user_id not in user_data:
        referral_code = generate_referral_code()
        user_data[user_id] = {
            'name': name,
            'referral_code': referral_code,
            'balance': 0,
            'referred_by': None
        }
    if ref and not user_data[user_id]['referred_by']:

sk me, [4/13/2025 8:59 PM]
user_data[user_id]['referred_by'] = ref
        # Credit referral bonus
        user_data[user_id]['balance'] += 10
    message = f"Welcome {user_data[user_id]['name']}! Your account is ready."
    return jsonify({
        'message': message,
        'balance': user_data[user_id]['balance'],
        'referral_code': user_data[user_id]['referral_code'],
        'referred_by': user_data[user_id]['referred_by']
    })

# Upgrade mining endpoint.
@app.route('/upgrade', methods=['POST'])
def upgrade():
    data = request.get_json()
    user_id = data.get('user_id')
    user_data[user_id]['balance'] += 5
    message = "Mining upgraded! Bonus +5 DOD."
    return jsonify({'message': message, 'balance': user_data[user_id]['balance']})

# Tap mining endpoint.
@app.route('/tap', methods=['POST'])
def tap():
    data = request.get_json()
    user_id = data.get('user_id')
    user_data[user_id]['balance'] += 1
    message = "Tap mining activated! +1 DOD."
    return jsonify({'message': message, 'balance': user_data[user_id]['balance']})

# Spin mining endpoint.
@app.route('/spin', methods=['POST'])
def spin():
    data = request.get_json()
    user_id = data.get('user_id')
    reward = random.choice([0, 2, 3])
    user_data[user_id]['balance'] += reward
    message = f"Spin complete! You earned {reward} DOD."
    return jsonify({'message': message, 'balance': user_data[user_id]['balance']})

# Airdrop endpoint.
@app.route('/airdrop', methods=['POST'])
def airdrop():
    data = request.get_json()
    user_id = data.get('user_id')
    bonus = random.choice([1, 5, 10])
    user_data[user_id]['balance'] += bonus
    message = f"Airdrop received! +{bonus} DOD credited."
    return jsonify({'message': message, 'balance': user_data[user_id]['balance']})

# Generate referral link endpoint.
@app.route('/generate_referral', methods=['POST'])
def generate_referral():
    data = request.get_json()
    user_id = data.get('user_id')
    referral_code = user_data.get(user_id, {}).get('referral_code')
    referral_link = f"https://yourdomain.com/?ref={referral_code}"
    message = f"Your referral link: {referral_link}"
    return jsonify({'message': message, 'referral_code': referral_code, 'balance': user_data[user_id]['balance']})

# The index route serves the main page.
@app.route('/')
def index():
    return render_template_string(frontend_html)

if name == 'main':
    port = int(os.environ.get("PORT", 5000))
    # In production, remove debug=True and use a production WSGI server.
    app.run(host='0.0.0.0', port=port, debug=True)
