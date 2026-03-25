import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# App Configuration
st.set_page_config(page_title="Global Trade AI", layout="wide")
st.title("📈 Global Real-Time Trading App")

# Sidebar
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC-USD, AAPL):", "BTC-USD")
period = st.sidebar.selectbox("Period:", ["1d", "5d", "1mo", "1y"])

# Fetch Data
try:
    data = yf.download(symbol, period=period, interval="1m" if period=="1d" else "1d")
    
    if not data.empty:
        # Price Metric
        current_price = data['Close'].iloc[-1]
        st.metric(label=f"Current Price of {symbol}", value=f"${current_price:,.2f}")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])
        
        fig.update_layout(title=f"{symbol} Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Buy / Sell Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("BUY", use_container_width=True):
                st.success(f"Bought {symbol} at ${current_price:,.2f}")
        with col2:
            if st.button("SELL", use_container_width=True):
                st.error(f"Sold {symbol} at ${current_price:,.2f}")
    else:
        st.warning("No data found. Check the symbol.")

except Exception as e:
    st.error(f"Error: {e}")