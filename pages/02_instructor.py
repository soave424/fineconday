import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

st.set_page_config(layout="wide", page_icon="image/pre.png", initial_sidebar_state="collapsed")

# CSV 파일 경로 설정
CSV_PATH = st.secrets["CSV_FILE_PATH"]

st.markdown("""
    <style>
        /* 제목과 버튼을 가로로 배치하는 flex 컨테이너 */
        .title-button-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        /* "오프연수 홈으로" 버튼 스타일 */
        .home-button {
            background-color: #4c6ef5;
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
            background-color: #009879;
            color: #ffffff;
            text-align: left;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #009879;
        }
    </style>
""", unsafe_allow_html=True)

# 강좌 정보 사전 (강좌명, 강사명, 강좌 코드, 강의실 정보)
course_info = {
    # 선택 강좌 1
    "경제교육보드게임, 캐쉬플로우": ("박민수쌤", "a0001", "미정"),
    "내 아이의 금융 문해력 기르기": ("댈님", "a0002", "미정"),
    "창업과 투자 그리고 기업가정신까지!? 일석삼조 효과의 '어쩌다 초등 사장' 프로젝트": ("쭈니쌤", "a0003", "미정"),
    "왕초보도 따라하는 학급화폐 1년 로드맵": ("좋아유쌤", "a0004", "미정"),
    "도구없이 누구나 할 수 있는 교육마술": ("이화수쌤", "a0005", "미정"),
    "초등형 MBTI 클래시파이 : 웹개발스토리와 감정소진없이 학급경영하기": ("김태림쌤", "a0006", "미정"),
    
    # 선택 강좌 2
    "학교에서 시작하는 부수입 노하우": ("퇴근맨", "b0001", "미정"),
    "코로나 실전 투자 경험을 통해 배운 행복한 부자로 가는 길": ("노현진쌤", "b0002", "미정"),
    "이렇게만 따라하세요! 20대 내 집 마련 루트": ("가드닝쌤", "b0003", "미정"),
    "내집마련 도전기: 꿈을 현실로 만드는 첫걸음": ("먹태쌤", "b0004", "미정"),
    "은또링샘의 친절한 재무제표 분석 (feat. 미리 캔버스)": ("은또링쌤", "b0005", "미정"),
    
    # 선택 강좌 3
    "교사를 위한 퍼스널 브랜딩 & 꼬꼬무 부수입": ("진격의홍쌤", "c0001", "미정"),
    "미친 자에게 건배를: 부동산 투자에 미친 자의 이야기": ("다니쌤", "c0002", "미정"),
    "부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z": ("홍당무쌤", "c0003", "미정"),
    "소비형 인간에서 저축형 인간 마인드셋하기": ("따롱쌤", "c0004", "미정"),
    "선생님의 돈공부: 재무관리와 내 삶 기획하기": ("달구쌤", "c0005", "미정")
}



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

# 기본 열이 없을 경우 추가
required_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3', '등록']
for column in required_columns:
    if column not in data.columns:
        data[column] = ""

# 페이지 제목과 홈 버튼
st.markdown("""
    <div class="title-button-container">
        <h1>강좌 신청 조회 및 등록 관리</h1>
        <a href="/" class="home-button">오프연수 홈으로</a>
    </div>
""", unsafe_allow_html=True)

# 강좌 선택
selected_course = st.selectbox("강좌를 선택하세요:", options=list(course_info.keys()))
course_instructor, course_code, _ = course_info[selected_course]
display_course_name = f"{selected_course} ({course_instructor})"

# 강좌 코드 입력
entered_code = st.text_input("강좌 코드를 입력하세요", type="password")

# 조회 버튼이 눌리면 강좌 코드 확인 후 필터링 수행
if st.button("조회"):
    # 선택된 강좌 코드와 입력한 코드 확인
    if entered_code == course_code:
        # 선택된 강좌에 해당하는 신청자 필터링
        course_attendees = data[
            data[['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']].apply(
                lambda row: any(selected_course in str(course) for course in row), axis=1
            )
        ]

        # 강좌 신청 조회 코드의 일부 수정
        if not course_attendees.empty:
            # '등록' 열의 값이 정확히 "등록"인 경우 상단에 배치하고 나머지는 이름 가나다순으로 정렬
            course_attendees['등록상태'] = course_attendees['등록'].apply(lambda x: 1 if x.strip() == "등록" else 0)
            course_attendees = course_attendees.sort_values(
                by=['등록상태', '이름'], ascending=[False, True]
            ).drop(columns=['등록상태'])

            # 1부터 시작하는 인덱스 열 추가
            course_attendees = course_attendees.reset_index(drop=True)
            course_attendees['번호'] = course_attendees.index + 1

            # 필요한 열만 선택하여 '번호'를 포함하여 출력
            st.write(f"**'{display_course_name}' 강좌를 신청한 명단:**")
            st.table(course_attendees[['번호', '이름', '지역', '등록']])
        else:
            st.warning(f"'{display_course_name}' 강좌에 신청한 사람이 없습니다.")
    else:
        st.error("잘못된 강좌 코드입니다. 다시 입력해주세요.")