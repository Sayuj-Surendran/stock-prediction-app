import streamlit as st
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

st.title("📈 Stock Price Prediction App")

stock = st.text_input("Enter Stock Symbol", "AAPL")

if st.button("Predict"):

    data = yf.download(stock, start="2015-01-01", end="2024-01-01")
    data = data[['Close']]

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)

    X = []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i])

    X = np.array(X)

    # Simple model (retrain quickly)
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, LSTM

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, scaled_data[60:], epochs=1, batch_size=32, verbose=0)

    last_60 = scaled_data[-60:]
    last_60 = last_60.reshape(1, 60, 1)

    prediction = model.predict(last_60)
    prediction = scaler.inverse_transform(prediction)

    st.success(f"Next Day Predicted Price: {prediction[0][0]:.2f}")
