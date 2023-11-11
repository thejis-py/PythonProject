from flask import Flask, redirect, url_for, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
#config sql database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class users(db.Model):
      _id = db.Column("id", db.Integer, primary_key=True)
      username = db.Column("username", db.String(100))
      hash = db.Column("hash", db.String(100))
      cash = db.Column("cash", db.Float, default=10000)

      def __init__(self, username, hash, cash=10000):
            self.username = username
            self.hash = hash
            self.cash = cash

#config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template("layout.html")

@app.route("/register", methods=["POST", "GET"])
def register():
     if request.method == "POST":
           username = request.form.get("username")
           password = request.form.get("password")
           password_conf = request.form.get("password_conf")

           if not username:
                 return render_template("register.html", error_m = "Please provide username")
           if not password:
                 return render_template("register.html", error_m = "Please provide password")

           found_user = users.query.filter_by(username=username).first()
           if found_user:
                 return render_template("register.html", error_m = "Username is already exist")
           if password != password_conf:
                 return render_template("register.html", error_m = "Password not match")

           user = users(username, password)
           db.session.add(user)
           db.session.commit()

           return render_template("register.html", error_m = "successful")
     return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
# if form is submited
	if request.method == "POST":
		# record the user name
		session["username"] = request.form.get("username")
		# redirect to the main page
		return redirect("/")
	return render_template("login.html")

@app.route("/logout")
def logout():
	session["name"] = None
	return redirect("/")


if __name__ == "__main__":
    db.create_all()
    app.run()
