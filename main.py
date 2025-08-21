import streamlit as st
import yfinance as yf #type: ignore
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📊 Credit / Stock Risk Analysis Platform")

# Input: Multiple tickers comma-separated
tickers_input = st.text_input(
    "Enter stock tickers (comma separated, e.g. RELIANCE.NS,TCS.NS,INFY.NS)",
    "RELIANCE.NS,TCS.NS,INFY.NS"
)
tickers = [t.strip() for t in tickers_input.split(",")]

# RSI function
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Analyze each ticker
for ticker in tickers:
    st.subheader(f"📈 {ticker} Analysis")

    # Fetch stock data
    data = yf.download(ticker, period="6mo")
    if data.empty:
        st.warning(f"No data found for {ticker}")
        continue

    # Display last 5 rows
    st.write("Last 5 rows of stock data:")
    st.dataframe(data.tail())

    # Calculate RSI
    data['RSI'] = calculate_rsi(data)

    # Plot Close price + RSI
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(data.index, data['Close'], color='blue', label='Close Price')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close Price', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(data.index, data['RSI'], color='red', label='RSI')
    ax2.set_ylabel('RSI', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.axhline(70, color='grey', linestyle='--')
    ax2.axhline(30, color='grey', linestyle='--')

    fig.tight_layout()
    st.pyplot(fig)

    # Risk alerts
    last_rsi = data['RSI'].iloc[-1]
    if last_rsi > 70:
        st.error(f"⚠️ {ticker} is Overbought! (RSI = {last_rsi:.2f})")
    elif last_rsi < 30:
        st.success(f"✅ {ticker} is Oversold! (RSI = {last_rsi:.2f})")
    else:
        st.info(f"{ticker} RSI = {last_rsi:.2f}")
