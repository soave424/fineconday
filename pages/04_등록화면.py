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
    data = pd.read_csv(CSV_PATH)
    # Ensure the '등록' column is boolean (True/False) for compatibility
    if '등록' in data.columns:
        data['등록'] = data['등록'].astype(bool)
    else:
        data['등록'] = False  # Default to False if the column doesn't exist
    return data

# 데이터 로드 (세션 상태 초기화)
if "data" not in st.session_state:
    st.session_state.data = load_data()

# Access code verification
access_code = st.text_input("코드를 입력하세요", type="password")
if access_code == "z733":
    st.success("코드가 확인되었습니다. 각 강좌별 신청 인원수를 확인할 수 있습니다.")

    # 데이터 편집 기능 추가
    st.write("데이터 편집이 가능합니다. '등록' 열을 체크박스로 변경 후 '변경 사항 저장' 버튼을 눌러주세요.")
    # Toggle all "등록" values between True and False

    edited_data = st.data_editor(
        st.session_state.data,
        use_container_width=True,
        column_config={
            "등록": st.column_config.CheckboxColumn(label="등록 여부")
        }
    )

    # '변경 사항 저장' 버튼 클릭 시 동작
    if st.button("변경 사항 저장"):
        # 편집된 데이터를 CSV 파일에 저장하고 세션 상태도 업데이트
        edited_data.to_csv(CSV_PATH, index=False)
        st.session_state.data = edited_data  # 세션 상태에 변경된 데이터 반영
        st.success("변경 사항이 저장되었습니다!")
else:
    st.warning("올바른 코드를 입력하세요.")