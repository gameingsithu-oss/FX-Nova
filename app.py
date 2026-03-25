import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="FX Nova - Smart Trading", layout="wide")

st.title("📈 FX Nova - Global Real-Time Trading")

# Sidebar
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC-USD, EURUSD=X):", "BTC-USD")
period = st.sidebar.selectbox("Select Period:", ["1d", "5d", "1mo", "1y"])

try:
    # Fetch Data
    data = yf.download(symbol, period=period, interval="1m" if period == "1d" else "1h")
    
    if not data.empty:
        # Get latest price clearly
        last_row = data.iloc[-1]
        latest_price = float(last_row['Close'])
        
        # Display Metric
        st.metric(label=f"Current {symbol} Price", value=f"${latest_price:,.2f}")

        # Candlestick Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'])])
        fig.update_layout(title=f"{symbol} Live Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Money Making Section
        st.markdown("---")
        st.success("### 🚀 Start Trading & Earn Bonuses!")
        st.write("Join the world's leading trading platform today.")
        # Me link eka oyaage affiliate link ekata passe maru karanna
        st.link_button("Open Trading Account Now", "https://www.google.com") 
    else:
        st.warning("No data found. Check the symbol again.")

except Exception as e:
    st.error(f"Waiting for market data... (Error: {e})")
