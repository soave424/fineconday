import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from app import render_sidebar


st.set_page_config(layout="wide", page_icon="image/pre.png", initial_sidebar_state="expanded")


# 사이드바 로그인 상태 렌더링
render_sidebar()

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

# 페이지 스타일 및 사용자 입력
st.markdown("""
    <style>
        .title-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .home-button {
            background-color: #4ca2bf;
            color: white !important;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1rem;
            font-weight: bold;
        }
        .home-button:hover {
            background-color: #3b5cc6;
        }
       /* 테이블 스타일 */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 1.1em;
            font-family: sans-serif;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .styled-table th, .styled-table td {
            padding: 12px 15px;
            text-align: left;
        }
        .styled-table thead tr {
            background-color: #5eb4d6;
            color: #ffffff;
            text-align: left;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #e6f3f8;
        }
        .styled-table tbody tr:hover {
            background-color: #d6efff;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #5eb4d6;
        }
        .styled-table tbody tr.active-row {
            font-weight: bold;
            color: #5eb4d6;
        }
    </style>
""", unsafe_allow_html=True)
# If user is logged in, use their information directly from session_state
if st.session_state.get("is_logged_in"):
    name = st.session_state.get("name")
    code = st.session_state.get("code")  # Now using `code` from session_state
    
    # Filter user data by 'name' and 'code' columns
    user_data = data[(data['이름'] == name) & (data['코드'] == code)]
    
    if not user_data.empty:
        # Display user info and course list
        user_name = f"{name} ({user_data['지역'].iloc[0]})"
        courses = user_data[['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']].values.flatten()
        
    # 강좌 정보 사전
    course_info = {
        "초등형 MBTI 클래시파이 : 웹개발스토리와 감정소진없이 학급경영하기": ("김태림쌤", "미정","https://classify.co.kr/"),
        "창업과 투자 그리고 기업가정신까지!? 일석삼조 효과의 '어쩌다 초등 사장' 프로젝트": ("쭈니쌤", "미정","https://blog.naver.com/prologue/PrologueList.naver?blogId=wnsgud3061&skinType=&skinId=&from=menu&userSelectMenu=true"),
        "경제교육보드게임, 캐쉬플로우": ("박민수쌤", "미정",""),
        "왕초보도 따라하는 학급화폐 1년 로드맵": ("좋아유쌤", "미정","https://www.youtube.com/@YuDongHyunTV"),
        "내 아이의 금융 문해력 기르기": ("댈님", "미정",""),
        "도구없이 누구나 할 수 있는 교육마술": ("이화수쌤", "미정",""),
        "이렇게만 따라하세요! 20대 내 집 마련 루트": ("가드닝쌤", "미정",""),
        "코로나 실전 투자 경험을 통해 배운 행복한 부자로 가는 길": ("노현진쌤", "미정",""),
        "은또링샘의 친절한 재무제표 분석 (feat. 미리 캔버스)": ("은또링쌤", "미정",""),
        "내집마련 도전기: 꿈을 현실로 만드는 첫걸음": ("먹태쌤", "미정",""),
        "학교에서 시작하는 부수입 노하우": ("퇴근맨", "미정",""),
        "부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z": ("홍당무쌤", "미정",""),
        "교사를 위한 퍼스널 브랜딩 & 꼬꼬무 부수입 by 진격의홍쌤": ("진격의홍쌤", "미정",""),
        "미친 자에게 건배를: 부동산 투자에 미친 자의 이야기": ("다니쌤", "미정",""),
        "소비형 인간에서 저축형 인간 마인드셋하기": ("따롱쌤", "미정",""),
        "선생님의 돈공부: 재무관리와 내 삶 기획하기": ("달구쌤", "미정","")
    }

    # 페이지 제목과 홈 버튼
    st.markdown("""
    <div class="title-container">
        <h1>강좌 시간표 확인</h1>
        <a href="/" target="_self" class="home-button">홈으로</a>
    </div>
""", unsafe_allow_html=True)

    # Prepare course data to display
    course_data = []
    for course in courses:
        if pd.notna(course):
            parts = course.split('/')
            course_name = parts[0].strip()
            instructor, classroom, link = course_info.get(course_name, ("", "미정", ""))
            
            # Create clickable link if available
            course_link = f"<a href='{link}' target='_blank'>{course_name}</a>" if link else course_name
            course_data.append({"강좌명": course_link, "강사명": instructor, "강의실": classroom})

        # Display course information as HTML table
        course_df = pd.DataFrame(course_data)
        course_df.index = course_df.index + 1
        st.write(f"{user_name}님의 강좌 목록:")
        st.markdown(course_df.to_html(escape=False, classes="styled-table"), unsafe_allow_html=True)

    else:
        st.warning("해당 이름과 코드에 해당하는 정보가 없습니다.")
else:
    # If not logged in, prompt for manual input
    st.info("로그인이 필요합니다. 사이드바에서 로그인하세요.")