import streamlit as st
import yfinance as yf
import requests
from datetime import datetime, timedelta

# ✅ Your Finnhub API Key
FINNHUB_API_KEY = "d2n5gg9r01qn3vmjhargd2n5gg9r01qn3vmjhas0"

@st.cache_data(ttl=3600)
def fetch_yahoo_news(ticker: str):
    """Attempt to fetch news from Yahoo Finance unofficial API."""
    url = f"https://query2.finance.yahoo.com/v6/finance/news?symbols={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        try:
            news = resp.json()
            if isinstance(news, dict):
                return news.get("items") or news.get("news") or []
        except ValueError:
            return None
    return None

@st.cache_data(ttl=3600)
def fetch_finnhub_news(ticker: str):
    """Fetch company news from Finnhub (fallback)."""
    today = datetime.utcnow().date()
    last_week = today - timedelta(days=7)
    url = (
        f"https://finnhub.io/api/v1/company-news"
        f"?symbol={ticker}"
        f"&from={last_week}"
        f"&to={today}"
        f"&token={FINNHUB_API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code == 200:
        try:
            return resp.json()
        except ValueError:
            return []
    return []

def format_unix_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %I:%M %p")
    except Exception:
        return str(ts)

# Streamlit UI
st.set_page_config(page_title="Live Stock News", layout="wide")
st.title("📊 Live Financial News")

st.sidebar.header("Stock Ticker")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()

st.sidebar.markdown("---")
st.sidebar.write("News will be fetched from Yahoo Finance if available, otherwise Finnhub (fallback).")

st.subheader(f"Live News for {ticker}")

# First try Yahoo
news_data = fetch_yahoo_news(ticker)

# If Yahoo fails, fall back to Finnhub
if not news_data:
    st.warning("Yahoo news unavailable or blocked. Falling back to Finnhub.")
    news_items = fetch_finnhub_news(ticker)
    source = "Finnhub"
else:
    news_items = news_data
    source = "Yahoo"

if news_items:
    for item in news_items:
        # Handle both Yahoo and Finnhub formats
        title = item.get("title") or item.get("headline") or "No Title Available"
        link = item.get("link") or item.get("url")
        publisher = item.get("publisher") or item.get("source", "Unknown Publisher")
        ts = item.get("providerPublishTime") or item.get("datetime")
        published = format_unix_timestamp(ts) if ts else "N/A"

        st.markdown(f"### {title}")
        st.write(f"**Publisher:** {publisher}")
        st.write(f"**Published:** {published}")
        if link:
            st.write(f"[Read more]({link})")
        st.markdown("---")
else:
    st.info(f"No news articles found via {source}.")
