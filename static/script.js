let tg = window.Telegram.WebApp;
tg.expand();

const user_id = tg.initDataUnsafe?.user?.id || Math.floor(Math.random() * 1000000);
const referrer_id = new URLSearchParams(window.location.search).get('ref');

document.addEventListener('DOMContentLoaded', () => {
  fetch('/start', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ user_id, referrer_id })
  }).then(() => {
    loadPoints();
    loadTON();
    document.getElementById('refLink').value = `${window.location.origin}/?ref=${user_id}`;
  });
});

function mine() {
  fetch('/mine', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ user_id })
  }).then(res => res.json())
    .then(data => {
      document.getElementById('points').innerText = `💰 Points: ${data.points}`;
    });
}

function loadPoints() {
  fetch('/get_points', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ user_id })
  }).then(res => res.json())
    .then(data => {
      document.getElementById('points').innerText = `💰 Points: ${data.points}`;
    });
}

function loadTON() {
  fetch('/ton_address')
    .then(res => res.json())
    .then(data => {
      document.getElementById('tonAddress').innerText = data.address;
    });
}

