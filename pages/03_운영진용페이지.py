import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from app import render_sidebar


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
    "초등형 MBTI 클래시파이 : 웹개발스토리와 감정소진없이 학급경영하기": ("김태림쌤", "6층 리더스홀","https://classify.co.kr/"),
    "창업과 투자 그리고 기업가정신까지!? 일석삼조 효과의 '어쩌다 초등 사장' 프로젝트": ("쭈니쌤", "6층 강의실","https://forms.gle/LZdgk5RTsYrB4Vov6"),
    "경제교육보드게임, 캐쉬플로우": ("박민수쌤", "7층 총회회의실",""),
    "왕초보도 따라하는 학급화폐 1년 로드맵": ("좋아유쌤", "7층 강의실B","https://www.youtube.com/@YuDongHyunTV"),
    "내 아이의 금융 문해력 기르기": ("댈님", "7층 강의실A",""),
    "도구없이 누구나 할 수 있는 교육마술": ("이화수쌤", "6층 휴게실",""),
    "이렇게만 따라하세요! 20대 내 집 마련 루트": ("가드닝쌤", "6층 리더스홀",""),
    "코로나 실전 투자 경험을 통해 배운 행복한 부자로 가는 길": ("노현진쌤", "7층 강의실B",""),
    "은또링샘의 친절한 재무제표 분석 (feat. 미리 캔버스)": ("은또링쌤", "7층 강의실A",""),
    "내집마련 도전기: 꿈을 현실로 만드는 첫걸음": ("먹태쌤", "6층 강의실",""),
    "학교에서 시작하는 부수입 노하우": ("퇴근맨", "미정",""),
    "부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z": ("홍당무쌤", "7층 강의실B","https://naver.me/G1wVwLL6"),
    "교사를 위한 퍼스널 브랜딩 & 꼬꼬무 부수입 by 진격의홍쌤": ("진격의홍쌤", "6층 리더스홀",""),
    "미친 자에게 건배를: 부동산 투자에 미친 자의 이야기": ("다니쌤", "7층 강의실A",""),
    "소비형 인간에서 저축형 인간 마인드셋하기": ("따롱쌤", "6층 강의실",""),
    "선생님의 돈공부: 재무관리와 내 삶 기획하기": ("달구쌤", "7층 총회회의실","")
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

# Access code verification
access_code = st.text_input("코드를 입력하세요", type="password")
if access_code == "z733":
    st.success("코드가 확인되었습니다. 각 강좌별 신청 인원수를 확인할 수 있습니다.")
    # Calculate the total number of attendees
    total_attendees = int(course_counts_df['신청 인원수'].sum()/3)

  # Display the DataFrame with column headers that can be clicked for sorting
    st.write(f"### 강좌별 신청 인원수 (총원: {total_attendees}명)")
    st.dataframe(course_counts_df[['강좌명', '강사명', '신청 인원수', '강좌 코드', '장소']], use_container_width=True, height=600)
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

    # Button links for additional resources
    st.markdown("""
        <div class="button-container">
            <a class="button-link" href="https://docs.google.com/spreadsheets/d/15_EGHe3-wiHTzuQNksXGdxkVtr9_JqSOao_I9TGfcXw/edit" target="_blank">신청시트원본</a>
            <a class="button-link" href="https://docs.google.com/spreadsheets/d/161CSOh2xYR7wE5fz20gPeWFMTeZ94fFSr6F-k1cVYhg/edit?gid=0#gid=0" target="_blank">강좌별명단</a>
            <a class="button-link" href="https://docs.google.com/spreadsheets/d/1_xfjGFODkhM0YLj1LbIDhJV8ENgSmAz6JknI7Zhty2Q/edit?gid=456685248#gid=456685248" target="_blank">점심메뉴신청</a>
        </div>
        """, unsafe_allow_html=True)
    
     # Extract unique lunch options
    lunch_options = data['점심메뉴'].dropna().unique()

    # Select a lunch option
    selected_menu = st.selectbox("점심 메뉴를 선택하세요:", lunch_options)

    # Filter data for the selected lunch menu
    filtered_data = data[data['점심메뉴'] == selected_menu]

    if not filtered_data.empty:
        st.write(f"**'{selected_menu}' 메뉴를 선택한 명단:**")

        # Add a checkbox for each row to display name (region - registration status)
        for idx, row in filtered_data.iterrows():
            registered_status = "true" if row['등록'] else "false"
            label = f"{row['이름']} ({row['지역']} - {registered_status})"
            st.checkbox(label, key=f"{row['이름']}_{row['지역']}")
    else:
        st.warning(f"'{selected_menu}' 메뉴를 선택한 사용자가 없습니다.")

else:
    st.warning("올바른 코드를 입력하세요.")