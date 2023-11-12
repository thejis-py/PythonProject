from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session as FlaskSession
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import lookup

#api=DM8J043TJV3OYW8H
app = Flask(__name__)

#config sql database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#users table
class Users(db.Model):
      _id = db.Column(db.Integer, primary_key=True)
      _username = db.Column(db.String(50), unique=True)
      _hash = db.Column(db.String())
      _cash = db.Column(db.Float)

      def __init__(self, username, hash, cash=10000):
            self._username = username
            self._hash = hash
            self._cash = cash
      def __repr__(self):
            return f"({self._id}) {self._username} {self._hash} {self._cash}"


#print data
with app.app_context():
      #Users.query.delete()
      users = Users.query.all()
      db.session.commit()
      print("testt")
      for i in users:
            print(i)

#config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
FlaskSession(app)

@app.route("/")
def home():
    return render_template("index.html")

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

           found_user = Users.query.filter_by(_username=username).first()

           if found_user:
                 print("-----found_user",found_user._id)
                 return render_template("register.html", error_m = "Username is already exist")
           if password != password_conf:
                 return render_template("register.html", error_m = "Password not match")

           new_user = Users(username, generate_password_hash(password))
           with app.app_context():
                  db.session.add(new_user)
                  db.session.commit()
           session["user_id"] = Users.query.filter_by(_username=username).first()._id

           return redirect("/")
     return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
# if form is submited
      session.clear()
      if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if not username:
                  return render_template("login.html", error_m = "Please provide username")
            if not password:
                  return render_template("login.html", error_m = "Please provide password")
            found_user = Users.query.filter_by(_username=username).first()
            if not found_user:
                  return render_template("login.html", error_m="Username not found")
            if not check_password_hash(found_user._hash, password):
                  return render_template("login.html", error_m="Incorrect Password")
            session["user_id"] = found_user._id
            return redirect("/")
      return render_template("login.html")

@app.route("/logout")
def logout():
      #forget session user_id
      session.clear()

      return redirect("/")

if __name__ == "__main__":
      with app.app_context():
            db.create_all()
      app.run()

