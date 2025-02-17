# Stockle_Project 
(Stockkle = Stock + Google 구글의 자유도 높은 검색을 주식 검색에) 

## 🎥시뮬레이션 
![화면 기록 2025-02-17 오후 4 31 29](https://github.com/user-attachments/assets/e90d0c05-4de1-41ca-9ee2-73c5c0627259)


## **🚀 프로젝트 개요**

📌 **목적:**

•	Streamlit을 활용하여 **사용자가 종목코드를 선택하면 실시간으로 주식 차트를 조회**할 수 있는 웹 애플리케이션 구축

•	yfinance를 사용하여 **Yahoo Finance에서 주식 데이터를 가져와 시각화**

•	**Elasticsearch를 활용한 주식 데이터 검색 최적화**

• **회사명, 업종, 주요제품 등을 tokenizer로 분석하여 자유도 높은 검색 구현**

•	한국거래소(KRX)에서 최신 종목코드 데이터를 수집하여 반영

## 📌 **사용 기술:**

•	**Elasticsearch (Nori Tokenizer, Mapping 설정, Reindexing)**

•	**Python (Streamlit, Pandas, yfinance, Plotly)**

•	**한국거래소(KRX) 종목코드 수집 (pandas.read_html)**

•	**DataFrame 내 종목코드 선택 기능 (st.data_editor())**

•	**캔들차트 (plotly.graph_objects.Candlestick)**

## **1. 한국거래소(KRX)에서 최신 종목코드 가져오기**

📌 **기능:**

✅ 한국거래소에서 **최신 상장 종목 데이터를 가져와 반영**

✅ pandas.read_html()을 사용하여 **KRX 웹사이트에서 데이터를 크롤링**

✅ **종목코드 6자리 포맷 유지** (005930 → 005930.KS 변환)

📌 **문제점 및 해결 방법:**

- ❌ **KRX 웹페이지 변경 시 데이터가 정상적으로 수집되지 않을 수 있음**
- ✅ **웹페이지 구조 변경 시 read_html()에서 header, encoding 등의 옵션을 수정하여 해결 가능**

## **2. Elasticsearch 인덱스 설정 및 Nori Tokenizer 적용**

📌 **기능:**

✅ **주식 데이터를 저장할 stock_info_nori 인덱스 생성**

✅ **Nori Tokenizer 적용하여 한글 데이터를 효과적으로 검색 가능하도록 설정**

✅ **불필요한 필드 (상장일, 결산월, 대표자명, 홈페이지, 지역) 삭제하여 데이터 최적화**

📌 **문제점 및 해결 방법:**

- ❌ **기존 인덱스에서 불필요한 필드가 많아 검색 최적화가 어려움**
- ✅ **Nori Tokenizer 적용 후 한글 검색 성능 개선 및 필요 필드만 유지하여 검색 효율 향상**

## **3. 기존 데이터에서 불필요한 필드 삭제 후 Reindexing**

📌 **기능:**

✅ **기존 stock_info 인덱스를 stock_info_nori로 마이그레이션하며 필요한 필드만 유지**

✅ **Elasticsearch의 _reindex API를 사용하여 데이터 복사**

📌 **문제점 및 해결 방법:**

- ❌ **Reindexing 수행 중 일부 데이터가 누락되는 문제 발생**
- ✅ **필요한 필드만 _source 옵션을 활용하여 선택적으로 복사하여 해결**

## **4. 종목코드 선택 기능 구현 (st.data_editor)**

📌 **기능:**

✅ **사용자가 DataFrame 내 체크박스를 클릭하면 종목을 선택할 수 있도록 구현**

✅ **선택된 종목의 데이터를 가져와 자동으로 차트를 업데이트**

📌 **문제점 및 해결 방법:**

- ❌ **기존 DataFrame에서 특정 행을 클릭해도 이벤트가 발생하지 않음**
- ✅ **st.data_editor()에 CheckboxColumn을 추가하여 선택 기능 구현**

## **5. yfinance를 활용한 주식 데이터 수집 및 MultiIndex 문제 해결**

📌 **기능:**

✅ **yfinance.download()를 사용하여 Yahoo Finance에서 주식 데이터 가져오기**

✅ **MultiIndex 문제 해결 (xs() 사용하여 단일 컬럼 변환)**

📌 **문제점 및 해결 방법:**

- ❌ **yfinance에서 Open, High, Low, Close 컬럼이 없는 문제 발생**
- ✅ **MultiIndex 구조에서 xs()를 활용하여 Ticker 인덱스를 제거하고 단일 컬럼 변환하여 해결**
- ✅ **Adj Close만 제공되는 경우 Close 컬럼으로 변환하여 차트 표시 가능하도록 개선**

## **6. Plotly를 활용한 캔들차트 시각화**

📌 **기능:**

✅ **plotly.graph_objects.Candlestick을 사용하여 주식 데이터를 캔들차트로 시각화**

✅ **Streamlit에서 st.plotly_chart(fig)로 차트 출력**

📌 **문제점 및 해결 방법:**

- ❌ **데이터가 부족하면 차트가 표시되지 않는 문제 발생**
- ✅ **최근 5일 데이터만 표시하도록 설정 (stock_data.tail(5))하여 해결**

## **🔥 최종 결과**

**Streamlit에서 종목을 선택하면, Elasticsearch에서 최적화된 데이터를 가져와 주식 차트를 확인할 수 있습니다!**
