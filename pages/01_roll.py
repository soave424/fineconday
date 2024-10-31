import streamlit as st
import pandas as pd
import os

# CSV 파일 경로 설정
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# CSV 파일을 불러오는 함수
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        st.success("CSV 파일을 성공적으로 불러왔습니다!")
        st.write(f"총 행 수: {len(df)}")
        return df
    else:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return None

# 데이터 로드 및 확인
data = load_data()

if data is not None:
    st.write(data.head())  # 데이터가 있을 경우 상위 5개 행을 출력
