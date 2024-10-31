import streamlit as st
import pandas as pd
import os

# 환경 변수에서 CSV 파일 경로 가져오기
CSV_PATH = st.secrets["CSV_FILE_PATH"]

@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()

# 데이터 로드
data = load_data()

st.write("현재 작업 디렉토리:", os.getcwd())
st.write("현재 디렉토리의 파일 목록:", os.listdir('.'))
