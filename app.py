import streamlit as st
import yfinance as yf

st.title("📈 Stock Price Predictor")

stock = st.text_input("Enter Stock Symbol", "AAPL")

if st.button("Predict"):
    data = yf.download(stock, start="2020-01-01", end="2024-01-01")

    if data.empty:
        st.error("Invalid stock symbol")
    else:
        last_price = data['Close'].iloc[-1]
        st.success(f"Latest Price: {last_price:.2f}")
