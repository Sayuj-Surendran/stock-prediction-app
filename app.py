import streamlit as st
import yfinance as yf

st.title("Stock Price Viewer")

stock = st.text_input("Enter Stock Symbol", "AAPL")

if st.button("Get Price"):
    data = yf.download(stock, period="5d")

    if data.empty:
        st.error("Invalid stock symbol")
    else:
        st.write(data.tail())
