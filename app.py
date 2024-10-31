import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# 페이지 설정
st.set_page_config(
    page_title="경제금융교육연구회",
    page_icon="image/pre.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 탭 생성
tab1, tab2, tab3 = st.tabs(["공지", "강좌 정보", "찾아오는 길"])

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
            <a class="button-link" href="https://bit.ly/econo1109" target="_blank">연수후기 남기기🖼</a>
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
    """)
    st.image("image/maininfo.jpg", caption="메인포스터", use_column_width=True)

# 탭 2: 강좌 정보
with tab2:
    st.header("강좌 정보")
    st.image("image/special.png", caption="강좌 안내", use_column_width=True)

# 탭 3: 찾아오는 길
with tab3:
    st.header("찾아오는 길")
    st.markdown("""
    ✅ **장소**: 전국투자자교육협의회 6, 7층  
    (서울 영등포구 여의나루로 67-8)  
    지하철 이용 시: 여의도역(5, 9호선) 4번 출구 이용
    """)
    st.image("image/map.png", caption="", use_column_width=True)
