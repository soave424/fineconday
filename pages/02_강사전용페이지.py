import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from app import render_sidebar


st.set_page_config(layout="wide", page_icon="image/pre.png", initial_sidebar_state="expanded")



# CSV 파일 경로 설정
load_dotenv()
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# Initialize session state for login tracking
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.user_type = None
    st.session_state.name = ""
    st.session_state.entrance_code = ""


st.markdown("""
    <style>
        .title-button-container {
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
            color: #f1f1f1 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 강좌 정보 사전
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
    "교사를 위한 퍼스널 브랜딩 & 꼬꼬무 부수입": ("진격의홍쌤", "c0001", "미정"),
    "미친 자에게 건배를: 부동산 투자에 미친 자의 이야기": ("다니쌤", "c0002", "미정"),
    "부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z": ("홍당무쌤", "c0003", "미정"),
    "소비형 인간에서 저축형 인간 마인드셋하기": ("따롱쌤", "c0004", "미정"),
    "선생님의 돈공부: 재무관리와 내 삶 기획하기": ("달구쌤", "c0005", "미정")
}

# CSV 파일 로드 함수
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()

# 데이터 로드
data = load_data()

# 기본 열이 없을 경우 추가
required_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3', '등록']
for column in required_columns:
    if column not in data.columns:
        data[column] = ""

# # 페이지 제목과 홈 버튼
# st.markdown("""
#     <div class="title-button-container">
#         <h1>강사전용 페이지</h1>
#         <a href="/" class="home-button">홈으로</a>
#     </div>
# """, unsafe_allow_html=True)

# 강사 인증 및 명단 조회 로직
if st.session_state.is_logged_in and st.session_state.user_type == "강사":
    # 사이드바에서 강사 코드 가져오기
    instructor_code = st.session_state.get("code", "").strip()
    
    # 강사 코드에 해당하는 강좌를 찾기
    selected_course, instructor_name = None, None
    for course_name, (name, code, _) in course_info.items():
        if code == instructor_code:
            selected_course = course_name
            instructor_name = name
            break
    
    if selected_course:
        # 강좌명과 강사명으로 제목 표시
        display_course_name = f"{selected_course} ({instructor_name})"
        st.write(f"### {display_course_name} 신청자 명단")

        # 선택된 강좌의 신청자 필터링
        course_attendees = data[
            data[['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']].apply(
                lambda row: any(selected_course in str(course) for course in row), axis=1
            )
        ]

        if not course_attendees.empty:
            # 등록 상태에 따라 정렬
            course_attendees['등록상태'] = course_attendees['등록'].apply(lambda x: 1 if x is True else 0)
            sorted_course_attendees = course_attendees.sort_values(
                by=['등록상태', '이름'], ascending=[False, True]
            ).drop(columns=['등록상태'])
            sorted_course_attendees = sorted_course_attendees.reset_index(drop=True)
            sorted_course_attendees['번호'] = sorted_course_attendees.index + 1

            # 테이블 출력
            st.table(sorted_course_attendees[['번호', '이름', '지역', '등록']].set_index('번호'))
        else:
            st.warning(f"'{display_course_name}' 강좌에 신청한 사람이 없습니다.")
    else:
        st.error("강사 코드와 일치하는 강좌가 없습니다.")
else:
    st.warning("강사 전용 페이지입니다. 사이드바에서 로그인해 주세요.")