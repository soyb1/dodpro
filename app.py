from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to a secure value!
app.permanent_session_lifetime = timedelta(days=365)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session.permanent = True
            session["username"] = username
            return redirect(url_for("home"))
    return render_template("login.html")  # Initial login screen

@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("index.html", username=username)

@app.route("/ton")
def ton_transaction():
    return redirect("https://tonkeeper.com/transfer/UQAL6w9kbYSioAM_jXk91CXt6Akdam8j88C6LxdYBa-Z7nrH")

if __name__ == "__main__":
    app.run(debug=True)
