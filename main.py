from flask import Flask, request
app = Flask(__name__)
from datetime import date
import yfinance as yf
import pandas as pd


START = "2020-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

@app.route('/')
def index():
    return '<h1>Utility to Retrieve Stock Data</h1>'

@app.route('/price/<ticker>')
def get_price(ticker):
    df = yf.download(ticker, START, TODAY)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.resample('2w').mean()
    
    chart1 = df['Close']
    chart2 = df['Close'].rolling(window = 12).mean().dropna()
    chart3 = df['Close'].rolling(window = 12).std().dropna()

    df_con = pd.concat([chart1, chart2, chart3], axis=1)
    df_con.columns=['Close', 'Rolling Mean', 'Rolling Std']
    df_con.reset_index(inplace=True)
    return df_con.to_json()


if __name__ == "__main__":
    app.run(debug=True)