from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session as FlaskSession
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import lookup, login_required, thb, dtformat
from datetime import datetime

#api=DM8J043TJV3OYW8H
app = Flask(__name__)
app.jinja_env.filters["thb"] = thb
app.jinja_env.filters["dt"] = dtformat

#config sql database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#users table
class Users(db.Model):
      #__tablename__ = "users"
      _id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(50), unique=True)
      hash = db.Column(db.String())
      cash = db.Column(db.Float)

      def __init__(self, username, hash, cash=10000):
            self.username = username
            self.hash = hash
            self.cash = cash
      def __repr__(self):
            return f"({self._id}) {self.username} {self.hash} {self.cash}"
class Portfolio(db.Model):
      #__tablename__ = "porfolio"

      _id = db.Column(db.Integer, primary_key=True)
      symbol = db.Column(db.String(50))
      amount = db.Column(db.Integer)
      purchase_price = db.Column(db.Float)
      user_id = db.Column(db.Integer)

      def __init__(self, symbol, amount, purchase_price, user_id):
            self.symbol = symbol
            self.amount = amount
            self.purchase_price = purchase_price
            self.user_id = user_id
      def __repr__(self):
            return f"({self._id}) {self.symbol} {self.amount} {self.purchase_price} {self.user_id}"
class History(db.Model):
      _id = db.Column(db.Integer, primary_key=True)
      side = db.Column(db.String)
      symbol = db.Column(db.String(50))
      price = db.Column(db.Float)
      amount = db.Column(db.Integer)
      time = db.Column(db.DateTime)
      user_id = db.Column(db.Integer)

      def __init__(self, side, symbol, price, amount, user_id):
            self.side = side
            self.symbol = symbol
            self.price = price
            self.amount = amount
            self.time = datetime.now()
            self.user_id = user_id

#create table if not exist
with app.app_context():
      db.create_all()

"""
#print data
with app.app_context():
      #Users.query.delete()
      users = Users.query.all()
      db.session.commit()
      print("testt")
      for i in users:
            print(i)
      port = Portfolio.query.all()
      db.session.commit()

      for i in port:
            print(i)
      history = History.query.all()
      db.session.commit()
      for i in history:
            print("his",i)

"""

#config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
FlaskSession(app)


@app.route("/history")
@login_required
def history():
      db.session.commit()
      return render_template("history.html", history = History.query.filter_by(user_id=session["user_id"]).order_by(History.time.desc()))

@app.route("/sell", methods=["POST", "GET"])
@login_required
def sell():
      if request.method == "POST":
            symbol = request.form.get("symbol").upper()
            amount = int(request.form.get("amount"))
            with app.app_context():
                  history = History("Sell", symbol, lookup(symbol)["price"], amount, session["user_id"])
                  db.session.add(history)

                  found_symbol = Portfolio.query.filter_by(user_id=session["user_id"], symbol=symbol).first()
                  found_symbol.purchase_price -= amount*(found_symbol.purchase_price/found_symbol.amount)
                  found_symbol.amount -= amount

                  db.session.commit()
                  if found_symbol.amount == 0:
                        Portfolio.query.filter_by(user_id=session["user_id"], symbol=symbol).delete()
                  db.session.commit()

                  return redirect("/history")
      return render_template("sell.html", portfolio=Portfolio.query.filter_by(user_id=session["user_id"]).order_by(Portfolio.symbol))

@app.route("/buy", methods=["POST", "GET"])
@login_required
def buy():
      if request.method == "POST":
            symbol = request.form.get("symbol").upper()
            amount = int(request.form.get("amount"))
            with app.app_context():
                  history = History("Buy", symbol, lookup(symbol)["price"], amount, session["user_id"])
                  db.session.add(history)

                  found_symbol = Portfolio.query.filter_by(user_id=session["user_id"], symbol=symbol).first()
                  if not found_symbol:
                        new_port = Portfolio(symbol, amount, round(float(lookup(symbol)["price"])*amount, 2), session["user_id"])
                        db.session.add(new_port)
                        db.session.commit()
                        return redirect("/")
                  found_symbol.purchase_price += round(lookup(symbol)["price"]*amount, 2)
                  found_symbol.amount += amount

                  db.session.commit()

                  return redirect("/history")
      return render_template("buy.html")

@app.route("/", methods=["POST", "GET"])
@login_required
def home():
      if request.method=="POST":
            return render_template("quoted.html", data = lookup(request.form.get("query")))

      user_port = Portfolio.query.filter_by(user_id = session["user_id"])

      price = {}
      total = {}
      unreal = {}
      for i in user_port:
            price[i.symbol] = (lookup(i.symbol)["price"])
            total[i.symbol] = (lookup(i.symbol)["price"])*i.amount
            unreal[i.symbol] = total[i.symbol]-i.purchase_price

      print(price)

      return render_template("index.html", data=user_port, price = price, total=total, unreal=unreal)

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

           found_user = Users.query.filter_by(username=username).first()

           if found_user:
                 return render_template("register.html", error_m = "Username is already exist")
           if password != password_conf:
                 return render_template("register.html", error_m = "Password not match")

           new_user = Users(username, generate_password_hash(password))
           with app.app_context():
                  db.session.add(new_user)
                  db.session.commit()

           session["user_id"] = Users.query.filter_by(username=username).first()._id

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

            found_user = Users.query.filter_by(username=username).first()
            if not found_user:
                  return render_template("login.html", error_m="Username not found")
            if not check_password_hash(found_user.hash, password):
                  return render_template("login.html", error_m="Incorrect Password")
            session["user_id"] = found_user._id
            return redirect("/")
      return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
      #forget session user_id
      session.clear()

      return redirect("/")

if __name__ == "__main__":
      app.run()

