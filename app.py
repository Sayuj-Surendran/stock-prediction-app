
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 Smart Stock Analyzer")

# Input
stock = st.text_input("Enter Stock Symbol", "AAPL")

# Time range selection
period = st.selectbox("Select Time Period", ["1mo", "6mo", "1y", "5y"])

if st.button("Get Price"):

    # Fetch data
    data = yf.download(stock, period=period)

    if data.empty:
        st.error("Invalid stock symbol")

    else:
        # Show last few rows
        st.subheader("📄 Recent Data")
        st.write(data.tail())

        # 📊 Latest Price
        latest_price = data['Close'].values[-1]
        st.metric("💰 Latest Price", f"{latest_price:.2f}")

        # 📈 Stock Price Chart
        st.subheader("📊 Stock Price Chart")
        plt.figure()
        plt.plot(data['Close'])
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(f"{stock} Price Trend")
        st.pyplot(plt)

        # 📉 Moving Average
        data['MA50'] = data['Close'].rolling(50).mean()

        st.subheader("📉 Moving Average (50 Days)")
        plt.figure()
        plt.plot(data['Close'], label="Close Price")
        plt.plot(data['MA50'], label="MA50")
        plt.legend()
        st.pyplot(plt)

        # 🔮 Simple Prediction
        prediction = data['Close'].values[-1] * 1.01
        st.subheader("🔮 Next Day Prediction")
        st.write("Predicted Price:", round(prediction, 2))


# 🔄 Multiple Stock Comparison
st.subheader("📊 Compare Multiple Stocks")

stocks = st.multiselect("Select Stocks", ["AAPL", "TSLA", "GOOG"])

for s in stocks:
    d = yf.download(s, period="1y")
    st.write(f"### {s}")
    st.line_chart(d['Close'])
