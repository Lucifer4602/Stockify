import streamlit as st
import yfinance as yf
import requests
import json

def fetch_yahoo_finance_news(ticker="AAPL"):
    """
    Fetch live finance news using Yahoo Finance.
    This example focuses on a specific stock ticker like 'AAPL' for Apple.
    """
    ticker_obj = yf.Ticker(ticker)
    news = ticker_obj.news  # Get news related to the ticker
    return news

# Streamlit app
st.set_page_config(page_title="Yahoo Finance Live News", layout="wide")
st.title("📊 Yahoo Finance: Live Financial News")

# Sidebar for stock ticker input
st.sidebar.header("Choose Stock Ticker")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")

st.sidebar.markdown("---")
st.sidebar.info("Get the latest financial news from Yahoo Finance for the chosen stock ticker.")

# Fetch and display news
st.subheader(f"Live News for {ticker.upper()}")
news_data = fetch_yahoo_finance_news(ticker)

if news_data:
    for news_item in news_data:
        st.markdown(f"### {news_item['title']}")
        st.write(news_item["publisher"])
        st.write(f"Published: {news_item['providerPublishTime']}")
        st.write(f"[Read more]({news_item['link']})")
        st.markdown("---")
else:
    st.info("No news articles available for this ticker at the moment.")
