import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

st.set_page_config(layout="wide", page_icon="image/pre.png", initial_sidebar_state="collapsed")

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

# 사용자 입력으로 코드 확인
access_code = st.text_input("코드를 입력하세요", type="password")

if access_code == "z733":
    st.success("코드가 확인되었습니다. 각 강좌별 신청 인원수를 확인할 수 있습니다.")

    if data.empty:
        st.warning("데이터가 비어 있거나 CSV 파일을 찾을 수 없습니다.")
    else:
        # 강좌 정보 딕셔너리 설정
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

        # 각 강좌별 신청 인원 계산
        course_columns = ['선택 강좌 1', '선택 강좌 2', '선택 강좌 3']
        course_counts = data[course_columns].melt(value_name='강좌명').dropna()['강좌명'].value_counts()

        # 강좌명과 인원수를 데이터프레임으로 변환
        course_counts_df = pd.DataFrame(course_counts).reset_index()
        course_counts_df.columns = ['강좌명', '신청 인원수']  # 열 이름 지정

        # 강좌 코드 열 추가
        course_counts_df['강좌 코드'] = course_counts_df['강좌명'].apply(lambda x: course_info.get(x, ("", ""))[1])

        # 정렬 방식 선택
        sort_option = st.radio("정렬 방식 선택", ["인원수별", "시간 순서 (강좌 코드 순)"])

        if sort_option == "인원수별":
            sorted_df = course_counts_df.sort_values(by='신청 인원수', ascending=False).reset_index(drop=True)
            st.table(sorted_df[['강좌명', '신청 인원수', '강좌 코드']])
        else:
            # 강좌 코드 순 정렬 및 구분선 추가
            sorted_df = course_counts_df.sort_values(by='강좌 코드').reset_index(drop=True)
            st.title("강좌 코드 순으로 정렬된 신청 인원수")

            current_code_prefix = None
            for index, row in sorted_df.iterrows():
                code_prefix = row['강좌 코드'][0] if row['강좌 코드'] else ""
                
                if code_prefix != current_code_prefix:
                    if current_code_prefix is not None:
                        st.markdown("---")  # 구분선 추가
                    st.subheader(f"강좌 코드 '{code_prefix}' 시작 강좌 목록")
                    current_code_prefix = code_prefix
                
                # 강좌명, 신청 인원수, 강좌 코드를 표 형식으로 출력
                st.write(f"- **강좌명**: {row['강좌명']}  |  **신청 인원수**: {row['신청 인원수']}  |  **강좌 코드**: {row['강좌 코드']}")

else:
    st.warning("올바른 코드를 입력하세요.")