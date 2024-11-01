import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# CSV 파일 경로
CSV_PATH = os.getenv("CSV_FILE_PATH", "data.csv")

# 데이터 로드 함수
def load_data():
    return pd.read_csv(CSV_PATH)

# 데이터 로드
if "data" not in st.session_state:
    st.session_state.data = load_data()

# 데이터 편집 기능 추가
edited_data = st.data_editor(st.session_state.data, use_container_width=True)

# '등록' 열에 대한 편집 결과 확인
if st.button("변경 사항 저장"):
    # 편집된 데이터를 CSV에 저장하고 세션 상태도 업데이트
    edited_data.to_csv(CSV_PATH, index=False)
    st.session_state.data = edited_data  # 변경된 데이터를 세션 상태에 반영
    st.success("변경 사항이 저장되었습니다!")
