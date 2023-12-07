import yfinance as yf
import streamlit as st


title = st.text_input('Give me stock ID', 'GOOGL')
st.write('The current movie title is', title)

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and ***volume*** of """ + title + """!"""

)

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'AAPL'
#get data on this ticker
tickerData = yf.Ticker(title)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price of """ + title
)
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price of """ + title
)
st.line_chart(tickerDf.Volume)