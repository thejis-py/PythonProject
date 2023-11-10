from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! tst"

@app.route("/<name>")
def user(name):
    return name

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="TETT"))

@app.route("/test")
def test():
    return redirect("home")

if __name__ == "__main__":
    app.run()

#hello