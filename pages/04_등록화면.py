import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# CSV 파일 경로
CSV_PATH = os.getenv("CSV_FILE_PATH", "data.csv")

# CSV 파일 로드 함수
def load_data():
    return pd.read_csv(CSV_PATH)

# 데이터 로드
data = load_data()

# '등록' 열이 없는 경우 False 값으로 초기화하고, 데이터 타입을 bool로 설정
if '등록' not in data.columns:
    data['등록'] = False
else:
    data['등록'] = data['등록'].astype(bool)  # "등록" 열을 bool 타입으로 변환

# 데이터 편집 기능 추가
# '등록' 열을 체크박스로 표시하도록 설정
edited_data = st.data_editor(
    data,
    column_config={
        "등록": st.column_config.CheckboxColumn("등록 여부")  # "등록" 열을 체크박스로 표시
    },
    use_container_width=True
)

# '등록' 열에 대한 편집 결과 확인 및 CSV 저장
if st.button("변경 사항 저장"):
    # 편집된 데이터를 CSV에 저장
    edited_data.to_csv(CSV_PATH, index=False)
    st.success("변경 사항이 저장되었습니다!")
