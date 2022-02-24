from flask import Flask, request
app = Flask(__name__)
from datetime import date
import yfinance as yf
import pandas as pd


START = "2019-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
stocks = ("AAPL", "GOOG", "MSFT", "TSLA")


@app.route('/')
def index():
    return '<h1>Utility to Retrieve Stock Data</h1>'

@app.route('/price/<ticker>')
def get_price(ticker):
    df = yf.download(ticker, START, TODAY)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df.to_json()


if __name__ == "__main__":
    app.run(debug=True)