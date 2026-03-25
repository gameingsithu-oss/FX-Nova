import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="FX Nova - Virtual Trading", layout="wide")

st.title("📈 FX Nova - Smart Paper Trading")

# Sidebar
st.sidebar.header("Trading Terminal")
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC-USD, ETH-USD):", "BTC-USD")

# Session State for Paper Trading (Virtual Balance)
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0  # Start with $10,000 virtual cash
if 'position' not in st.session_state:
    st.session_state.position = 0.0

try:
    # Fetch Data
    data = yf.download(symbol, period="1d", interval="1m")
    
    if not data.empty:
        latest_price = float(data['Close'].iloc[-1])
        
        # Display Virtual Wallet
        col1, col2, col3 = st.columns(3)
        col1.metric("Virtual Balance", f"${st.session_state.balance:,.2f}")
        col2.metric("Current Price", f"${latest_price:,.2f}")
        col3.metric("Your Position", f"{st.session_state.position} {symbol.split('-')[0]}")

        # Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
        st.plotly_chart(fig, use_container_width=True)

        # Trading Buttons
        st.subheader("Place a Virtual Trade")
        t_col1, t_col2 = st.columns(2)
        
        with t_col1:
            if st.button(f"BUY {symbol.split('-')[0]}", use_container_width=True):
                if st.session_state.balance >= latest_price:
                    st.session_state.balance -= latest_price
                    st.session_state.position += 1
                    st.success(f"Bought 1 {symbol}!")
                else:
                    st.error("Not enough balance!")

        with t_col2:
            if st.button(f"SELL {symbol.split('-')[0]}", use_container_width=True):
                if st.session_state.position > 0:
                    st.session_state.balance += latest_price
                    st.session_state.position -= 1
                    st.warning(f"Sold 1 {symbol}!")
                else:
                    st.error("Nothing to sell!")

    st.info("💡 Note: This is a virtual trading simulator for practice. No real money involved.")

except Exception as e:
    st.error(f"Waiting for market: {e}")
