import streamlit as st
import os

# CSV 파일 경로 가져오기
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# CSV 파일 경로 확인
if not os.path.exists(CSV_PATH):
    st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
else:
    st.write("CSV 파일 경로:", CSV_PATH)
