
import os
import json
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import plotly.express as px

from app.__init__ import to_usd

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")

def get_response(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url) # issues an HTTP request
    return json.loads(response.text)

if __name__ == "__main__":

    # FETCH DATA

    symbol = input("Please input a stock symbol (e.g. 'MSFT'): ")
    parsed_response = get_response(symbol)
    #request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    #response = requests.get(request_url)
    #parsed_response = json.loads(response.text)
    
    # PROCESS DATA
    
    records = []
    for date, daily_data in parsed_response["Time Series (Daily)"].items():
        record = {
            "date": date,
            "open": float(daily_data["1. open"]),
            "high": float(daily_data["2. high"]),
            "low": float(daily_data["3. low"]),
            "close": float(daily_data["4. close"]),
            "volume": int(daily_data["5. volume"]),
        }
        records.append(record)
    
    df = DataFrame(records)
    
    # DISPLAY RESULTS
    
    #print("LATEST CLOSING PRICE: ", to_usd(records[0]["close"]))
    print("LATEST CLOSING PRICE: ", to_usd(df.iloc[0]["close"]))
    print("RECENT HIGH: ", to_usd(df["high"].max()))
    print("RECENT LOW: ", to_usd(df["low"].min()))
    
    # EXPORT PRICES TO CSV
    
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol.lower()}_prices.csv")
    df.to_csv(csv_filepath)
    
    # CHART PRICES OVER TIME
    
    fig = px.line(df, y="close", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
    fig.show()
    