function startApp() {
  const username = document.getElementById("username").value.trim();
  if (!username) {
    alert("Please enter a username.");
    return;
  }

  localStorage.setItem("username", username);
  document.getElementById("user-name-display").innerText = username;
  document.getElementById("login-screen").classList.add("hidden");
  document.getElementById("main-screen").classList.remove("hidden");
}

function showTasks() {
  document.getElementById("content-area").innerHTML = `
    <h3>Tasks</h3>
    <ul>
      <li>✅ Join our Telegram Channel</li>
      <li>✅ Follow us on Twitter</li>
      <li>🔄 Complete daily mining</li>
    </ul>
  `;
}

function showReferrals() {
  const username = localStorage.getItem("username") || "user";
  document.getElementById("content-area").innerHTML = `
    <h3>Referral System</h3>
    <p>Share your referral link:</p>
    <input value="https://t.me/YOUR_BOT_USERNAME?start=${username}" readonly />
  `;
}

function showMining() {
  let power = parseInt(localStorage.getItem("power") || "0");

  document.getElementById("content-area").innerHTML = `
    <h3>Mining</h3>
    <p>Tap the rock to mine DOD tokens!</p>
    <div style="margin: 20px;">
      <button onclick="mineDOD()">⛏️ Tap to Mine</button>
      <p id="power-display">${power} DOD</p>
    </div>
    <a href="ton://transfer/UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH" style="color: #fff; text-decoration: underline;" target="_blank">Send TON</a>
  `;
}

function mineDOD() {
  let power = parseInt(localStorage.getItem("power") || "0");
  power += 1;
  localStorage.setItem("power", power);
  document.getElementById("power-display").innerText = `${power} DOD`;
}

function showLeaderboard() {
  document.getElementById("content-area").innerHTML = `
    <h3>Leaderboard</h3>
    <p>Coming soon...</p>
  `;
}

function showAirdrop() {
  document.getElementById("content-area").innerHTML = `
    <h3>Airdrop</h3>
    <p>🎁 Big surprise coming soon. Stay tuned!</p>
  `;
}

// Auto login if already in localStorage
window.onload = () => {
  const username = localStorage.getItem("username");
  if (username) {
    document.getElementById("user-name-display").innerText = username;
    document.getElementById("login-screen").classList.add("hidden");
    document.getElementById("main-screen").classList.remove("hidden");
  }
};
