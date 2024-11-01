import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# 페이지 설정
st.set_page_config(
    page_title="경제금융교육연구회",
    page_icon="image/pre.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sidebar logo
st.sidebar.image("image/logo.png", use_column_width=True)

# Main body logo
st.image("image/mainlogo.jpg", use_column_width=True)

# Optional link in the sidebar
st.sidebar.markdown("[Visit our community](https://cafe.naver.com/financialeducation)")


# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["✅공지", "📚강좌 정보", "🗺️찾아오는 길","🍲점심 안내", "🍻뒷풀이 신청"])

# 탭 1: 공지
with tab1:
    st.header("공지사항")

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

    # 버튼 3개를 한 줄에 꽉 차게 배치
    st.markdown(
        """
        <div class="button-container">
            <a class="button-link" href="https://241109.streamlit.app/roll" target="_self">강좌신청 확인하기🔍</a>
            <a class="button-link" href="https://open.kakao.com/o/g141aCVg" target="_blank">오픈채팅방 입장👨🏻‍💻</a>
            <a class="button-link" href="https://bit.ly/econo1109" target="_blank">연수 질문&후기📜</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 일시 및 장소
    st.subheader("📅 일시 및 장소")
    st.markdown("""
    ✅ **일시**: 2024. 11. 9. (토) 10:30~17:40  
    *(끝나고 희망자에 한해 뒤풀이도 있어요!!!🍺)*

    ✅ **장소**: 전국투자자교육협의회 6, 7층  
    (서울 영등포구 여의나루로 67-8)  
    지하철 이용 시: 여의도역(5, 9호선) 4번 출구 이용
                
    ✅ 참가 신청 (신청 마감)
    참가비 25,000원을 납부하셔야 최종 신청이 됩니다.
    참가비 납부 계좌: 카카오뱅크(김성훈) 7979-48-04052 혹은 3333-0394-2925
    (*입금 시 입금자명 뒤에 전화번호 네 자리 입력 요청드립니다 /
    행사 운영을 위해 환불 요청은 10월 31일까지만 가능함을 양해바랍니다)

    ✅ 준비물 : 필기도구
    몇 몇 강의는 별도로 강의안을 인쇄해 나눠드릴 예정입니다.
    전체 교안과 PPT는 따로 제공되지 않습니다.
    """)
    st.image("image/maininfo.jpg", caption="메인포스터", use_column_width=True)

# 탭 2: 강좌 정보
with tab2:
    st.header("강좌 정보")
    st.image("image/special.png", caption="특강 안내", use_column_width=True)
    st.image("image/select1.png", caption="선택강좌 1 안내", use_column_width=True)
    st.image("image/select2.png", caption="선택강좌 2 안내", use_column_width=True)
    st.image("image/select3.png", caption="선택강좌 3 안내", use_column_width=True)

# 탭 3: 찾아오는 길
with tab3:
    st.header("찾아오는 길")
    st.markdown("""
    ✅ **장소**: 전국투자자교육협의회 6, 7층  
    (서울 영등포구 여의나루로 67-8)  
    지하철 이용 시: 여의도역(5, 9호선) 4번 출구 이용
    """)
    st.image("image/map.png", caption="", use_column_width=True)

# 탭 4: 점심 안내
with tab4:
    st.header("점심 안내")
    
    st.markdown("""
    ✅ 점심 식사
    참가 확정 후 희망하는 분들에 한해
    도시락 및 근처 식당 예약을 받고 있습니다. 
    """)
    st.markdown(
    """
    <div class="button-container">
        <a class="button-link" href="https://forms.gle/QfXYQrMgHWakHfux8" target="_self">점심메뉴 신청하기🌯</a>
    </div>
    """,
    unsafe_allow_html=True
)
    st.image("image/menu.png", caption="", use_column_width=True)


# 탭 5: 뒷풀이 신청
with tab5:
    st.header("뒷풀이 신청")