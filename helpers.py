from flask import redirect, render_template, request
import requests
import urllib.parse

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