import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Smart Stock Analyzer", layout="wide")

# Custom UI Styling
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #ffffff;
}
.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<p class="title">📈 Smart Stock Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyze stock trends, compare companies & view predictions</p>', unsafe_allow_html=True)
st.markdown("---")

# Input Section
col1, col2 = st.columns(2)

with col1:
    stock = st.text_input("🔎 Enter Stock Symbol", "AAPL")

with col2:
    period = st.selectbox("📅 Select Time Period", ["1mo", "6mo", "1y", "5y"])

# Button
if st.button("🚀 Analyze Stock"):

    data = yf.download(stock, period=period)

    if data.empty:
        st.error("❌ Invalid stock symbol")

    else:
        st.success("✅ Data Loaded Successfully")

        # ✅ FIX CLOSE COLUMN (handles multi-column issue)
        close_data = data['Close']
        if hasattr(close_data, "columns"):
            close_data = close_data.iloc[:, 0]

        close_data = close_data.dropna()

        if len(close_data) == 0:
            st.error("❌ No valid price data")
            st.stop()

        # ✅ Latest price & prediction
        latest_price = float(close_data.iloc[-1])
        prediction = latest_price * 1.01

        col1, col2 = st.columns(2)

        with col1:
            st.metric("💰 Latest Price", f"{latest_price:.2f}")

        with col2:
            st.metric("🔮 Predicted Price", f"{prediction:.2f}")

        st.markdown("---")

        # 📊 Stock Chart
        st.subheader("📊 Stock Price Trend")

        plt.figure(figsize=(10,4))
        plt.plot(close_data)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid()
        st.pyplot(plt)

        # 📉 Moving Average
        data['MA50'] = close_data.rolling(50).mean()

        st.subheader("📉 Moving Average (50 Days)")

        plt.figure(figsize=(10,4))
        plt.plot(close_data, label="Close Price")
        plt.plot(data['MA50'], label="MA50")
        plt.legend()
        plt.grid()
        st.pyplot(plt)

        # 📄 Recent Data
        st.subheader("📄 Recent Data")
        st.dataframe(data.tail())

# Divider
st.markdown("---")

# 📊 Stock Comparison
st.subheader("📊 Compare Multiple Stocks")

stocks = st.multiselect("Select Stocks", ["AAPL", "TSLA", "GOOG"])

if stocks:
    cols = st.columns(len(stocks))

    for i, s in enumerate(stocks):
        d = yf.download(s, period="1y")

        if not d.empty:
            c = d['Close']
            if hasattr(c, "columns"):
                c = c.iloc[:, 0]

            with cols[i]:
                st.write(f"### {s}")
                st.line_chart(c)
