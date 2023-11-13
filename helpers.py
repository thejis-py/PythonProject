from flask import redirect, render_template, request, session
import requests
import urllib.parse
from functools import wraps

def lookup(symbol):

    # Contact API
    try:
        api_key = "pk_82dc7e2d3e374584aea3abe1a2a6de78"
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        print("In1")
    except requests.RequestException:
        return None
    print("OUT")
    # Parse response
    try:
        quote = response.json()
        print("In2")
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


# Python program to convert the currency
# of one country to that of another country

# Import the modules needed
import requests

class Currency_convertor:
	# empty dict to store the conversion rates
    rates = {}
    def __init__(self, url):
        data = requests.get(url).json()

		# Extracting only the rates from the json data
        self.rates = data["rates"]

	# function to do a simple cross multiplication between
	# the amount and the conversion rates
    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'EUR' :
            amount = float(amount) / self.rates[from_currency]
		# limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        return amount


def thb(value):
    """Format value as THB."""
    #c.convert(from_country, to_country, amount)
    #currency exchange api:3c866d2732c59e2ea6883b7125c60ef4
    currency_api = "3c866d2732c59e2ea6883b7125c60ef4"
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', currency_api)
    c = Currency_convertor(url)
    value = c.convert("USD","THB", value)

    #c.convert(from_country, to_country, amount)
    return f"฿{value:,.2f}"

def dtformat(time):
    """format datetime"""
    time = str(time).split()
    time[1] = time[1].split(".")[0]
    return " ".join(time)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    """
    #alpha vantage
    try:
        #find the best match
        api = "DM8J043TJV3OYW8H"
        api_iex = "pk_82dc7e2d3e374584aea3abe1a2a6de78"
        url_symbol = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={name}&apikey={api}'
        print("URL", url_symbol)
    except:
        print("except lookup")
        return None
    print(requests.get(url_symbol).json(), "TESTTTTTTT")
    info = requests.get(url_symbol).json()["bestMatches"][0]
    print("___info", info)

    #search stock's data
    symbol = info["1. symbol"]
    url_data = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api}"
    data = requests.get(url_data).json()["Global Quote"]
    print("----data", data)

    print(info["1. symbol"], info["2. name"], data["05. price"])

    return {
        "symbol": symbol,
        "company_name": info["2. name"],
        "lastest_price": data["05. price"]
    }
    """