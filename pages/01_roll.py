import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# 환경 변수 설정 로드
load_dotenv()

# 환경 변수에서 CSV 파일 경로 불러오기
CSV_PATH = os.getenv('CSV_FILE_PATH', 'data/hidden_data.csv')

# CSV 파일 불러오기 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        st.success("CSV 파일 로드 성공!")
        return df
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()

# 데이터 불러오기 및 확인
data = load_data()

# 데이터가 잘 불러와졌는지 확인하기 위해 미리보기 출력
if not data.empty:
    st.write("CSV 파일 데이터 미리보기:")
    st.dataframe(data.head())  # 상위 5개 행만 미리보기
else:
    st.warning("데이터가 없습니다.")
