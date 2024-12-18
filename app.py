import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os


# CSV 파일 경로 설정
load_dotenv()
CSV_PATH = st.secrets["CSV_FILE_PATH"]

# 페이지 설정
st.set_page_config(
    page_title="경제금융교육연구회",
    page_icon="image/pre.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("image/logo.png", size="large", link="https://cafe.naver.com/financialeducation")


# Initialize session state for login tracking
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.user_type = None
    st.session_state.name = ""
    st.session_state.entrance_code = ""
    st.session_state.lunch=""
if "lunch_menu" not in st.session_state:
    st.session_state.lunch_menu = ""  # 기본값 설정

# CSV 파일 로드 함수
# @st.cache_data
# CSV 파일 로드 함수 (매번 새로 로드하도록 설정)
def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        df['이름'] = df['이름'].str.strip()
        df['입장코드'] = df['입장코드'].astype(str).str.strip()
        df['입장코드'] = df['입장코드'].astype(str).str.zfill(4)
        df.to_csv(CSV_PATH, index=False)


        return df
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return pd.DataFrame()


# 데이터 로드
data = load_data()


# 로그인 함수
def login():
    name = st.session_state.input_name.strip()
    entrance_code = st.session_state.input_ecode.strip()
    
    # Filter user data based on name and 입장코드
    user_data = data[(data['이름'] == name) & (data['입장코드'] == entrance_code)]

    if not user_data.empty:
        # Set session state upon successful login
        st.session_state.is_logged_in = True
        st.session_state.name = name
        st.session_state.entrance_code = entrance_code
        st.session_state.user_type = user_data.iloc[0]['분류']
        st.session_state.lunch_menu = user_data['점심메뉴'].values[0]
    else:
        st.sidebar.error(f"이름 또는 입장코드가 잘못되었습니다. 다시 입력해주세요. (이름: {name}, 입장코드: {entrance_code})")

# Logout function to reset session state
def logout():
    st.session_state.is_logged_in = False
    st.session_state.user_type = None
    st.session_state.name = ""
    st.session_state.entrance_code = ""
    st.session_state.lunch_menu=""

# Sidebar login UI rendering function
def render_sidebar():
    with st.sidebar:
        if not st.session_state.is_logged_in:
            st.radio("로그인 유형 선택", ["연수참여", "강사", "운영지원"], key="user_type_selection")
            st.text_input("이름", key="input_name")
            st.text_input("입장코드(핸드폰 마지막 4자리 또는 강사코드)", key="input_ecode", type="password")
            if st.button("로그인"):
                login()
        else:
            # Display a personalized welcome message
            user_type_message = {
                "연수참여": "경금교 연수에 오신 것을 환영합니다.",
                "강사": "오늘 연수 힘내세요!",
                "운영지원": "오늘 하루 힘내세요!"
            }
            welcome_message = user_type_message.get(st.session_state.user_type, "환영합니다!")
            st.sidebar.success(f"{st.session_state.name} 선생님! ({st.session_state.entrance_code}) {welcome_message}")
            if st.button("로그아웃"):
                logout()

# 메인 페이지에서 사이드바 렌더링
render_sidebar()

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["✅공지", "📚강의", "🗺️찾아오는 길","🍲점심", "🍻뒤풀이"])

# 점심 메뉴와 대응 이미지, 설명 매핑
menu_details = {
    "샌드위치: 서브웨이 에그마요세트 (샌드위치+콜라 구성, 4,800원)": {
        "image": "lunch1egg.png",
        "message": "* 선생님이 선택하신 메뉴는 서브웨이 에그마요세트입니다. 강의실에서 식사 후 자리 뒷정리 부탁 드립니다!"
    },
    "식당: 팔당반점(짜장면, 5,000원)": {
        "image": "lunch2zz.png",
        "message": "선생님이 선택하신 메뉴는 짜장면입니다. 12시 10분에 음식이 바로 나오니 팔당반점 여의도 BNK직영점(도보1분)으로 늦게 않게 오세요~ "
    },
    "식당: 팔당반점(짬뽕, 7,000원)": {
        "image": "lunch3bb.png",
        "message": "선생님이 선택하신 메뉴는 짬뽕입니다. 12시 10분에 음식이 바로 나오니 팔당반점 여의도 BNK직영점(도보1분)으로 늦게 않게 오세요~ "
    },
    "제가 알아서 먹겠습니다!": {
        "image": "lunch4self.png",
        "message": "즐거운 식사 시간을 보내고 1시 10분에 만나요~"
    },
    "미응답": {
        "image": "",
        "message": "점심메뉴를 신청하지 않았습니다. 근처 식당을 이용해서 자유롭게 식사 후 1시 10분에 뵙겠습니다."
    }
}

# 탭 1: 공지
with tab1:
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
    st.header("공지사항")
    # 버튼 3개를 한 줄에 꽉 차게 배치
    st.markdown(
        """
        <div class="button-container">
            <a class="button-link" href="https://open.kakao.com/o/g141aCVg" target="_blank">오픈채팅방👨🏻‍💻</a>
            <a class="button-link" href="https://bit.ly/econo1109" target="_blank">질문/후기📜</a>
        </div>
        <div id="image-container" style="display:none; text-align:center;">
            <img src="image/show.jpg" alt="강좌 신청 확인 방법" style="max-width:100%;">
        </div>
        <script>
            function toggleImage() {
                var imgContainer = document.getElementById("image-container");
                if (imgContainer.style.display === "none") {
                    imgContainer.style.display = "block";
                } else {
                    imgContainer.style.display = "none";
                }
            }
        </script>
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
                
    ✅ 준비물 : 필기도구 (
    전체 교안과 PPT는 따로 제공되지 않습니다. 몇 몇 강의는 별도로 강의안을 인쇄해 나눠드릴 예정입니다.)
    특히 아래 강좌의 경우 꼭 필기도구를 준비해주세요.
    - 부린이도 할 수 있다! 같은 돈으로 더 오르는 내집 마련 A to Z(홍당무쌤) : 필기구
    - 선생님의 돈공부: 재무관리와 내 삶 기획하기(달구쌤) : 필기구
    - 내집마련 도전기: 꿈을 현실로 만드는 첫걸음(먹태쌤): 필기구
    - 경제교육보드게임, 캐쉬플로우(박민수쌤) : 연필, 지우개
    - 초등형 MBTI 클래시파이 : 웹개발스토리와 감정소진없이 학급경영하기(김태림) : 클래시파이 검사 진행 
                            
    ✅ 신청 강좌 확인하는 방법              
    """)
    st.image("image/show.png",use_column_width=True)
    st.image("image/maininfo.jpg", caption="메인포스터", use_column_width=True)

# 탭 2: 강좌 정보
with tab2:
    st.header("강좌 정보")
    st.image("image/special.png", caption="특강 안내", use_column_width=True)
    st.image("image/timetable.png",caption="강의실 안내", use_column_width=True)
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
    * 건물 주차장이 너무 협소해서 해당 건물에 주차는 어렵습니다. 
    """)
    st.image("image/map.png", caption="", use_column_width=True)

# 탭 4: 점심 안내
with tab4:
    selected_lunch_menu = st.session_state.lunch_menu
    st.header("점심 안내")
    if st.session_state.lunch_menu:
            # 점심 메뉴 정보 설정
            lunch_info = menu_details.get(selected_lunch_menu, {"image": "", "message": "선택한 점심 메뉴가 없습니다."})
            image_path = lunch_info["image"]
            message = lunch_info["message"]

            # 1:2 비율의 다단 레이아웃 구성
            col1, col2 = st.columns([1, 2])

            with col1:
                # 이미지가 있을 경우만 표시
                if image_path:
                    st.image(f"image/{image_path}", use_column_width=True)

            with col2:
                # 해당 메뉴 설명 메시지 표시
                st.write(message)

    else:
        # 로그인하지 않거나 선택된 메뉴가 없는 경우
        st.warning("로그인 후 점심 메뉴를 확인할 수 있습니다.")

# 탭 5: 뒤풀이 신청
with tab5:
    st.header("뒤풀이 신청_치맥(저녁 6시~)")
    if not st.session_state.is_logged_in:
        st.warning("로그인이 필요합니다. 사이드바에서 로그인해주세요.")
    else:
        # 로그인한 사용자의 데이터 필터링
        user_data = data[(data['이름'] == st.session_state.name) & (data['입장코드'] == st.session_state.entrance_code)]
        
        if user_data.empty:
            st.warning("해당 이름과 입장코드로 일치하는 정보를 찾을 수 없습니다.")
        else:
            # 뒤풀이 신청 상태 확인
            participates_in_party = user_data['뒤풀이참가'].iloc[0]
            payment_confirmed = user_data['뒤풀이입금'].iloc[0]
            
            # 조건에 따른 메시지 및 버튼 표시
            if not participates_in_party:
                st.info("뒤풀이에 함께 하고 싶다면 신청해주세요.")
                if st.button("뒤풀이 신청"):
                    # 뒤풀이참가를 True로 설정하고 CSV 업데이트
                    data.loc[(data['이름'] == st.session_state.name) & (data['입장코드'] == st.session_state.entrance_code), '뒤풀이참가'] = True
                    data.to_csv(CSV_PATH, index=False)
                    st.success("뒤풀이에 신청되었습니다! 참가비를 입금해주세요 : 3333063647260 카카오뱅크 (이조은) 참가비 2만원")
            elif participates_in_party and not payment_confirmed:
                st.info("참가비 확인 중입니다.")
                st.write("**입금 계좌: 3333063647260 카카오뱅크 (이조은),참가비 2만원 ")
            elif participates_in_party and payment_confirmed:
                st.success("참가가 확정되었습니다. 즐거운 시간 함께 더 보내요!")
