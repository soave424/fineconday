import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# CSV 파일 경로 설정
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# CSV 파일 로드 함수
# @st.cache_data
# CSV 파일 로드 함수 (매번 새로 로드하도록 설정)
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()

# 데이터 로드
data = load_data()

# 데이터가 로드되었는지 확인
if data.empty:
    st.warning("데이터가 비어 있거나 CSV 파일을 찾을 수 없습니다.")
else:
    # 각 강좌별 신청 인원 계산
    course_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']
    course_counts = data[course_columns].melt(value_name='강좌명').dropna()['강좌명'].value_counts()

    # 결과를 표로 표시
    st.title("각 강좌별 신청 인원수")
    st.table(course_counts.reset_index().rename(columns={'index': '강좌명', '강좌명': '신청 인원수'}))
