import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# CSV 파일 경로
CSV_PATH = os.getenv("CSV_FILE_PATH", "data.csv")

# CSV 파일 로드 함수
@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

# 데이터 로드
data = load_data()

# 데이터 편집 기능 추가
edited_data = st.data_editor(data, use_container_width=True)

# '등록' 열에 대한 편집 결과 확인
if st.button("변경 사항 저장"):
    # 편집된 데이터를 CSV에 저장
    edited_data.to_csv(CSV_PATH, index=False)
    st.success("변경 사항이 저장되었습니다!")
