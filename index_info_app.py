import streamlit as st
import pandas as pd
from elastic_api import search_index
import plotly.graph_objects as go
import yfinance as yf

def get_valid_stock_data(ticker):
    """
    종목코드가 `KQ` 또는 `KS`에서 데이터가 정상적으로 받아지는지 확인 후 반환.
    """
    for suffix in [".KQ", ".KS"]:
        test_ticker = ticker.split(".")[0] + suffix
        stock_data = yf.download(test_ticker, period="1mo", interval="1d", auto_adjust=False)
        if not stock_data.empty:
            # :흰색_확인_표시: MultiIndex 제거
            if isinstance(stock_data.columns, pd.MultiIndex):
                stock_data = stock_data.xs(key=test_ticker, axis=1, level=1)
            # :흰색_확인_표시: Close 컬럼이 없고 Adj Close만 있는 경우
            if "Close" not in stock_data.columns and "Adj Close" in stock_data.columns:
                stock_data["Close"] = stock_data["Adj Close"]
            # :흰색_확인_표시: Open, High, Low 컬럼이 없는 경우 Close 값으로 채움
            for col in ["Open", "High", "Low"]:
                if col not in stock_data.columns:
                    stock_data[col] = stock_data["Close"]
            return stock_data, test_ticker
    return None, ticker

st.set_page_config(page_title="주식 종합 검색", layout="centered")
# 기존 st.title 대신 HTML 마크업을 사용하여 제목을 가운데 정렬
st.markdown("<h1 style='text-align: center;'>📈 Stockle</h1>", unsafe_allow_html=True)

st.markdown("""
        <style>
            .search-container {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                height: auto;
                flex-direction: column;
                margin-top: 20px;
            }
            .search-box {
                width: 60%;
                max-width: 600px;
                text-align: center;
            }
            .stTextInput {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="search-container">', unsafe_allow_html=True)
match_name = st.text_input("", placeholder="Search...")
st.markdown('</div>', unsafe_allow_html=True)

if match_name:
    result = search_index('stock_info_nori', match_name)     

    if result.to_dict()["hits"]["hits"]:
        source_data = [entry["_source"] for entry in result.to_dict()["hits"]["hits"]]
        df = pd.DataFrame(source_data)
        df.insert(0, '선택', [False] * len(df))

        # Ensure '선택' column is boolean
        df['선택'] = df['선택'].astype(bool)

        edited_df = st.data_editor(
            df,
            num_rows="fixed",
            hide_index=True,
            column_config={"선택": st.column_config.CheckboxColumn("선택", help="조회할 종목을 선택하세요")},
            key="selected_stock"
        )
        
        # 선택된 종목 확인
        selected_rows = edited_df[edited_df["선택"]]

        if not selected_rows.empty:
            selected_stock_name = selected_rows.iloc[0]["회사명"]
            selected_stock_ticker = selected_rows.iloc[0]["종목코드"]
            st.subheader(f"{selected_stock_name} 주식 차트")
            stock_data, valid_ticker = get_valid_stock_data(selected_stock_ticker)
            if stock_data is not None:
                # 데이터 인덱스 변환
                stock_data.index = pd.to_datetime(stock_data.index)
                # `Open`, `High`, `Low`, `Close` 컬럼이 존재하는지 체크 후 `dropna()` 적용
                needed_columns = ["Open", "High", "Low", "Close"]
                available_columns = [col for col in needed_columns if col in stock_data.columns]
                if available_columns:
                    stock_data.dropna(subset=available_columns, inplace=True)
                if not stock_data.empty:
                    # 캔들차트 생성
                    fig = go.Figure(data=[go.Candlestick(
                        x=stock_data.index,
                        open=stock_data["Open"],
                        high=stock_data["High"],
                        low=stock_data["Low"],
                        close=stock_data["Close"],
                        name=valid_ticker
                    )])
                    # 차트 스타일 설정
                    fig.update_layout(
                        xaxis_rangeslider_visible=False,
                        xaxis_title="날짜",
                        yaxis_title="주가"
                    )
                    st.plotly_chart(fig)
                else:
                    st.warning("주식 데이터가 부족하여 차트를 표시할 수 없습니다.")
            else:
                st.error("해당 종목의 데이터를 가져올 수 없습니다. 종목코드를 확인하세요.")
    else:
        st.warning("검색 결과가 없습니다.")
