import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Premium Stock Analyzer", layout="wide")

# Custom UI
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #00FFAA;
}
.subtitle {
    text-align: center;
    color: #aaaaaa;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">📈 Premium Stock Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced stock insights with charts & predictions</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar controls
st.sidebar.header("⚙️ Controls")

stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
period = st.sidebar.selectbox("Select Time Period", ["1mo", "6mo", "1y", "5y"])

analyze = st.sidebar.button("🚀 Analyze")

# Main logic
if analyze:

    data = yf.download(stock, period=period)

    if data.empty:
        st.error("❌ Invalid stock symbol")

    else:
        st.success("✅ Data Loaded Successfully")

        close_data = data['Close'].dropna()
        latest_price = float(close_data.iloc[-1])
        prediction = latest_price * 1.01
        volume_data = data['Volume'].dropna()

        if len(volume_data) > 0:
        volume = int(volume_data.iloc[-1])
        else:
        volume = 0

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Price", f"{latest_price:.2f}")
        col2.metric("🔮 Prediction", f"{prediction:.2f}")
        col3.metric("📊 Volume", volume)

        st.markdown("---")

        # Candlestick Chart
        st.subheader("📊 Candlestick Chart")

        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])

        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Moving Average Chart
        data['MA50'] = data['Close'].rolling(50).mean()

        st.subheader("📉 Moving Average (50 Days)")

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close'))
        fig2.add_trace(go.Scatter(x=data.index, y=data['MA50'], name='MA50'))

        fig2.update_layout(template="plotly_dark")

        st.plotly_chart(fig2, use_container_width=True)

        # Recent Data
        st.subheader("📄 Recent Data")
        st.dataframe(data.tail())

# Divider
st.markdown("---")

# Stock Comparison
st.subheader("📊 Compare Multiple Stocks")

stocks = st.multiselect("Select Stocks", ["AAPL", "TSLA", "GOOG"])

if stocks:
    for s in stocks:
        d = yf.download(s, period="1y")
        st.write(f"### {s}")
        st.line_chart(d['Close'])
