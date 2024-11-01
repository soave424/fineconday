import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Page configuration
st.set_page_config(layout="wide", page_icon="image/pre.png", initial_sidebar_state="collapsed")

# Load environment variables
load_dotenv()

# Load the CSV file path from environment variables
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# Function to load data from the CSV file
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()

# Function to save data back to CSV
def save_data(data):
    data.to_csv(CSV_PATH, index=False)

# Load the data
data = load_data()

# Ensure '등록' column exists for True/False editing
if '등록' not in data.columns:
    data['등록'] = False  # 기본값 False로 설정

# Configure the AgGrid with editable "등록" column
st.write("### 강좌별 신청 인원수 (등록 수정 가능)")

# Set up AgGrid options
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_column("등록", editable=True)  # '등록' 열을 편집 가능하게 설정
grid_options = gb.build()

# Display editable AgGrid
grid_response = AgGrid(
    data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MANUAL,  # 변경 사항을 직접 저장할 수 있도록 설정
    data_return_mode=DataReturnMode.AS_INPUT,
)

# 데이터프레임 업데이트 후 저장
updated_data = grid_response['data']

# 저장 버튼을 누르면 CSV 파일에 변경사항 저장
if st.button("변경 사항 저장"):
    save_data(pd.DataFrame(updated_data))
    st.success("변경 사항이 저장되었습니다.")
