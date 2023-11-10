from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! test test"

@app.route("/<name>")
def user(name):
    return name

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="TESTTTTTTT"))

if __name__ == "__main__":
    app.run()
