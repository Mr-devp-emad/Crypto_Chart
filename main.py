import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=7&interval=daily"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = data.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        return df
    return None

def get_market_trend(df):
    if df is not None:
        price_change = df["price"].iloc[-1] - df["price"].iloc[0]
        if price_change > 0:
            return "📈 Market is Up - Consider Buying!"
        else:
            return "📉 Market is Down - Consider Selling!"
    return "No data available."

st.title("📊 Crypto Trading Suggestion App")
st.write("Search for a cryptocurrency and get price trends with Buy/Sell recommendations.")

crypto_id = st.text_input("Enter Crypto ID (e.g., bitcoin, ethereum, dogecoin)", "bitcoin")
if st.button("Get Data"):
    df = get_crypto_data(crypto_id)
    if df is not None:
        st.subheader(f"7-Day Price Trend for {crypto_id.capitalize()}")
        fig = px.line(df, x='timestamp', y='price', title=f"{crypto_id.capitalize()} Price Trend")
        st.plotly_chart(fig)
        
        suggestion = get_market_trend(df)
        st.subheader("Trading Suggestion:")
        st.write(suggestion)
    else:
        st.error("Invalid crypto ID or data not available. Try another currency.")
