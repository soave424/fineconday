import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

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

# Load the data
data = load_data()

# Define course information dictionary
course_info = {
    "경제교육보드게임, 캐쉬플로우": ("박민수쌤", "a0001", "미정"),
    "내 아이의 금융 문해력 기르기": ("댈님", "a0002", "미정"),
    "창업과 투자 그리고 기업가정신까지!? 일석삼조 효과의 '어쩌다 초등 사장' 프로젝트": ("쭈니쌤", "a0003", "미정"),
    "왕초보도 따라하는 학급화폐 1년 로드맵": ("좋아유쌤", "a0004", "미정"),
    "도구없이 누구나 할 수 있는 교육마술": ("이화수쌤", "a0005", "미정"),
    "초등형 MBTI 클래시파이 : 웹개발스토리와 감정소진없이 학급경영하기": ("김태림쌤", "a0006", "미정"),
    "학교에서 시작하는 부수입 노하우": ("퇴근맨", "b0001", "미정"),
    "코로나 실전 투자 경험을 통해 배운 행복한 부자로 가는 길": ("노현진쌤", "b0002", "미정"),
    "이렇게만 따라하세요! 20대 내 집 마련 루트": ("가드닝쌤", "b0003", "미정"),
    "내집마련 도전기: 꿈을 현실로 만드는 첫걸음": ("먹태쌤", "b0004", "미정"),
    "은또링샘의 친절한 재무제표 분석 (feat. 미리 캔버스)": ("은또링쌤", "b0005", "미정"),
    "교사를 위한 퍼스널 브랜딩 & 꼬꼬무 부수입 by 진격의홍쌤": ("진격의홍쌤", "c0001", "미정"),
    "미친 자에게 건배를: 부동산 투자에 미친 자의 이야기": ("다니쌤", "c0002", "미정"),
    "부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z": ("홍당무쌤", "c0003", "미정"),
    "소비형 인간에서 저축형 인간 마인드셋하기": ("따롱쌤", "c0004", "미정"),
    "선생님의 돈공부: 재무관리와 내 삶 기획하기": ("달구쌤", "c0005", "미정")
}

# Count attendees for each course
course_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']
course_counts = data[course_columns].melt(value_name='강좌명').dropna()['강좌명'].value_counts()

# Prepare DataFrame for display
course_counts_df = pd.DataFrame(course_counts).reset_index()
course_counts_df.columns = ['강좌명', '신청 인원수']

# Split 강좌명 and add details from course_info
course_counts_df[['강좌명', '강사명']] = course_counts_df['강좌명'].str.split('/', expand=True)
course_counts_df['강사명'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x.strip(), ("정보 없음",))[0])
course_counts_df['강좌 코드'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x.strip(), ("", "코드 없음",))[1])
course_counts_df['장소'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x.strip(), ("", "", "미정"))[2])

# Set default sorted_df for display before any button click
sorted_df = course_counts_df.copy()

# Initialize session state variables for sorting direction
if "sort_by_name_asc" not in st.session_state:
    st.session_state.sort_by_name_asc = True
if "sort_by_instructor_asc" not in st.session_state:
    st.session_state.sort_by_instructor_asc = True
if "sort_by_count_asc" not in st.session_state:
    st.session_state.sort_by_count_asc = True
if "sort_by_code_asc" not in st.session_state:
    st.session_state.sort_by_code_asc = True
if "sort_by_location_asc" not in st.session_state:
    st.session_state.sort_by_location_asc = True

# Access code verification
access_code = st.text_input("코드를 입력하세요", type="password")
if access_code == "z733":
    st.success("코드가 확인되었습니다. 각 강좌별 신청 인원수를 확인할 수 있습니다.")
    # Calculate the total number of attendees
    total_attendees = int(course_counts_df['신청 인원수'].sum()/3)

    # Display total attendees above the buttons
    st.write(f"### 총 신청자 수: {total_attendees}명")

# Data preparation for course information
course_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']
course_counts = data[course_columns].melt(value_name='강좌명').dropna()['강좌명'].value_counts()
course_counts_df = pd.DataFrame(course_counts).reset_index()
course_counts_df.columns = ['강좌명', '신청 인원수']
course_counts_df['강사명'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x, ("정보 없음",))[0])
course_counts_df['강좌 코드'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x, ("", "코드 없음",))[1])
course_counts_df['장소'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x, ("", "", "미정"))[2])

# Initialize sorting state in session
if "sort_by" not in st.session_state:
    st.session_state.sort_by = {"column": "강좌명", "asc": True}

# Sorting function
def sort_table(column):
    # Toggle sort direction if column is the same
    if st.session_state.sort_by["column"] == column:
        st.session_state.sort_by["asc"] = not st.session_state.sort_by["asc"]
    else:
        st.session_state.sort_by = {"column": column, "asc": True}
    # Sort dataframe
    return course_counts_df.sort_values(by=column, ascending=st.session_state.sort_by["asc"])

# CSS for table header buttons
st.markdown("""
    <style>
        .sortable-header {
            cursor: pointer;
            color: #009879;
            font-weight: bold;
            text-align: left;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Table header with buttons
st.markdown(f"""
    <div class="sortable-header">
        <span onclick="window.location.href='?sort_column=강좌명'">강좌명</span> |
        <span onclick="window.location.href='?sort_column=강사명'">강사명</span> |
        <span onclick="window.location.href='?sort_column=신청 인원수'">신청 인원수</span> |
        <span onclick="window.location.href='?sort_column=강좌 코드'">강좌 코드</span> |
        <span onclick="window.location.href='?sort_column=장소'">장소</span>
    </div>
""", unsafe_allow_html=True)

# Sort and display table
sorted_df = sort_table(st.session_state.sort_by["column"])
st.table(sorted_df[['강좌명', '강사명', '신청 인원수', '강좌 코드', '장소']])

 # 버튼 스타일 추가
    st.markdown("""
        <style>
            .button-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .button-link {
                background-color: #5eb4d6;
                color: white !important;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 1.1rem;
                font-weight: bold;
                text-align: center;
                text-decoration: none;
                flex: 1;
            }
            .button-link:hover {
                background-color: #4ca2bf;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="button-container">
            <a class="button-link" href="https://docs.google.com/spreadsheets/d/15_EGHe3-wiHTzuQNksXGdxkVtr9_JqSOao_I9TGfcXw/edit" target="_self">신청시트원본</a>
            <a class="button-link" href="https://docs.google.com/spreadsheets/d/161CSOh2xYR7wE5fz20gPeWFMTeZ94fFSr6F-k1cVYhg/edit?gid=0#gid=0" target="_self">강좌별명단</a>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.warning("올바른 코드를 입력하세요.")
