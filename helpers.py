from flask import redirect, render_template, request
import requests

def lookup(name):

    try:
        #find the best match
        api = "DM8J043TJV3OYW8H"
        url_symbol = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={name}&apikey={api}'
        info = requests.get(url_symbol).json()["bestMatches"][0]

        #search stock's data
        symbol = info["1. symbol"]
        url_data = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api}"
        data = requests.get(url_data).json()["Global Quote"]
    except:
        print("except lookup")
        return None

    print(info["1. symbol"], info["2. name"], data["05. price"])

    return {
        "symbol": symbol,
        "company_name": info["2. name"],
        "lastest_price": data["05. price"]
    }
