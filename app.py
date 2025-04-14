import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)  # Fix here: __name__ instead of name

# Your logo in Base64 format
logo_image_base64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAMAAADz"
    # Truncated for brevity...
)

# Your frontend HTML
frontend_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DOD Mining App</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
    }
    header {
      background-color: #333;
      color: #fff;
      text-align: center;
      padding: 10px;
    }
    header img {
      vertical-align: middle;
      max-height: 50px;
      margin-right: 10px;
    }
    .container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
    }
    .status {
      text-align: center;
      font-size: 1.2em;
      margin: 20px 0;
    }
    .buttons {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 15px;
    }
    .buttons button {
      padding: 15px 25px;
      font-size: 1em;
      border: none;
      border-radius: 8px;
      background-color: #007bff;
      color: #fff;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }
    .buttons button:hover {
      background-color: #0056b3;
    }
    footer {
      text-align: center;
      padding: 15px;
      font-size: 0.9em;
      color: #666;
    }
  </style>
</head>
<body>
  <header>
    <img src="{{ logo }}" alt="Logo">
    <span>DOD Mining App</span>
  </header>
  <div class="container">
    <p class="status" id="status">Coming Soon...</p>
    <div class="buttons">
      <button onclick="sendAction('upgrade')">Upgrade Mining</button>
      <button onclick="sendAction('tap')">Tap Mining</button>
      <button onclick="sendAction('spin')">Spin & Earn</button>
      <button onclick="sendAction('airdrop')">Airdrop</button>
    </div>
  </div>
  <footer>
    &copy; 2025 DOD Mining App. All rights reserved.
  </footer>
  <script>
    function sendAction(action) {
      fetch('/' + action, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          document.getElementById('status').innerText = data.message;
        })
        .catch(error => {
          document.getElementById('status').innerText = 'Error: ' + error;
        });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(frontend_html, logo=logo_image_base64)

@app.route('/upgrade', methods=['POST'])
def upgrade():
    return jsonify({'message': 'Mining upgraded. Power boosted!'})

@app.route('/tap', methods=['POST'])
def tap():
    return jsonify({'message': 'Tap mining activated! You earned 0.05 DOD.'})

@app.route('/spin', methods=['POST'])
def spin():
    return jsonify({'message': 'Spin complete! You earned 0.1 DOD.'})

@app.route('/airdrop', methods=['POST'])
def airdrop():
    return jsonify({'message': 'Airdrop initiated! Check your account soon.'})

if __name__ == '__main__':  # Fix here: use __name__ and __main__
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
