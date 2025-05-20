import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

st.title("글로벌 시가총액 TOP10 기업 - 최근 1년 주가 변화")

# 시가총액 상위 10개 글로벌 기업의 티커 (2024 기준)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'NVIDIA': 'NVDA',
    'Berkshire Hathaway': 'BRK-B',
    'Meta (Facebook)': 'META',
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 수집
@st.cache_data
def fetch_data(tickers):
    data = {}
    for name, ticker in tickers.items():
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            df['Name'] = name
            data[name] = df['Adj Close']
    return pd.DataFrame(data)

data = fetch_data(top10_tickers)

# 데이터가 정상적으로 로드되었는지 확인
if data.empty:
    st.warning("데이터를 불러올 수 없습니다. 인터넷 연결을 확인하세요.")
else:
    # Plotly 그래프
    fig = go.Figure()
    for col in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=col))

    fig.update_layout(
        title="최근 1년간 시가총액 TOP10 기업의 주가 변화",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        template="plotly_white"
    )

    st.plotly_chart(fig)
    st.markdown("데이터 출처: Yahoo Finance")
