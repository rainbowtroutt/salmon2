import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시가총액 Top10 주가 변화", layout="wide")
st.title("🌍 글로벌 시가총액 TOP10 기업 - 최근 1년 주가 변화")

# 시가총액 상위 10개 글로벌 기업의 티커 (2024 기준)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'NVIDIA': 'NVDA',
    'Berkshire Hathaway': 'BRK.B',  # 점으로 표기
    'Meta (Facebook)': 'META',
    'Tesla': 'TSLA',
    'TSMC': 'TSM'
}

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 수집 함수
@st.cache_data
def fetch_data(tickers):
    data = {}
    for name, ticker in tickers.items():
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        # 멀티 인덱스 대응
        if isinstance(df.columns, pd.MultiIndex):
            if 'Adj Close' in df.columns.get_level_values(0):
                series = df['Adj Close']
                if isinstance(series, pd.DataFrame):
                    data[name] = series.iloc[:, 0]
        elif 'Adj Close' in df.columns:
            data[name] = df['Adj Close']
    return pd.DataFrame(data)

# 데이터 불러오기
data = fetch_data(top10_tickers)

# 시각화
if data.empty:
    st.warning("❗ 데이터를 불러오지 못했습니다. 인터넷 연결 또는 티커명을 확인해주세요.")
else:
    fig = go.Figure()
    for company in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[company],
            mode='lines',
            name=company
        ))

    fig.update_layout(
        title="📈 최근 1년간 글로벌 시가총액 Top 10 기업의 주가 변화",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.2)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("🔎 데이터 출처: [Yahoo Finance](https://finance.yahoo.com)")
