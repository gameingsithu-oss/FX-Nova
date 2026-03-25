import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="FX Nova Pro - Terminal", layout="wide")

st.title("🚀 FX Nova - Smart Trading Terminal")

# Sidebar
st.sidebar.header("Market Selection")
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC-USD, DOGE-USD):", "DOGE-USD").upper()

# Advanced Session State
if 'balance' not in st.session_state:
    st.session_state.balance = 10000.0
if 'inventory' not in st.session_state:
    st.session_state.inventory = {}
if 'history' not in st.session_state:
    st.session_state.history = []

try:
    data = yf.download(symbol, period="1d", interval="1m")
    if not data.empty:
        # Fixed RSI Calculation
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi_series = 100 - (100 / (1 + rs))
        current_rsi = float(rsi_series.iloc[-1])

        latest_price = float(data['Close'].iloc[-1])
        
        # Portfolio Summary
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Available Cash", f"${st.session_state.balance:,.2f}")
        
        qty_owned = st.session_state.inventory.get(symbol, {}).get('qty', 0)
        avg_price = st.session_state.inventory.get(symbol, {}).get('avg_price', 0)
        
        col2.metric(f"{symbol} Owned", f"{qty_owned}")
        
        # Profit/Loss Calculation
        pl = (qty_owned * latest_price) - (qty_owned * avg_price)
        col3.metric("Profit / Loss", f"${pl:,.2f}", delta=f"{pl:,.2f}")
        col4.metric("Market Price", f"${latest_price:,.2f}")

        # RSI Signal Alert
        st.subheader("💡 Market Signal")
        if current_rsi < 30:
            st.success(f"🔥 BUY SIGNAL: {symbol} is Oversold (RSI: {current_rsi:.2f}). Good time to Buy!")
        elif current_rsi > 70:
            st.warning(f"⚠️ SELL SIGNAL: {symbol} is Overbought (RSI: {current_rsi:.2f}). Good time to Sell!")
        else:
            st.info(f"⚖️ NEUTRAL: Market is stable (RSI: {current_rsi:.2f}).")

        # Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Trading Panel
        st.subheader("⚡ Quick Trade")
        c1, c2 = st.columns(2)
        
        with c1:
            amount = st.number_input("Amount to Buy/Sell", min_value=0.01, step=1.0, value=100.0)
            if st.button(f"BUY {symbol}", use_container_width=True, type="primary"):
                cost = amount * latest_price
                if st.session_state.balance >= cost:
                    st.session_state.balance -= cost
                    old_qty = st.session_state.inventory.get(symbol, {}).get('qty', 0)
                    old_avg = st.session_state.inventory.get(symbol, {}).get('avg_price', 0)
                    new_qty = old_qty + amount
                    new_avg = ((old_avg * old_qty) + cost) / new_qty
                    st.session_state.inventory[symbol] = {'qty': new_qty, 'avg_price': new_avg}
                    st.session_state.history.append([datetime.now(), "BUY", symbol, amount, latest_price])
                    st.rerun()

        with c2:
            st.write(" ")
            if st.button(f"SELL {symbol}", use_container_width=True):
                if st.session_state.inventory.get(symbol, {}).get('qty', 0) >= amount:
                    st.session_state.balance += (amount * latest_price)
                    st.session_state.inventory[symbol]['qty'] -= amount
                    st.session_state.history.append([datetime.now(), "SELL", symbol, amount, latest_price])
                    st.rerun()
                else:
                    st.error("Not enough assets to sell!")

except Exception as e:
    st.error(f"Connecting to Market Data... {e}")
