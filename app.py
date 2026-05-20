import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="연애 초보 도우미",
    page_icon="💕",
)

# 제목
st.title("💕 연애 초보 도우미")
st.write("연애가 어려운 사람들을 위한 간단한 상담 앱!")

# 사용자 이름 입력
name = st.text_input("이름을 입력하세요")

# 상황 선택
situation = st.selectbox(
    "현재 상황을 선택하세요",
    ["썸 타는 중", "고백 고민 중", "연락이 어렵다", "데이트 준비 중"]
)

# 고민 입력
problem = st.text_area("현재 고민을 적어보세요")

# 호감도 슬라이더
interest = st.slider("상대방의 호감도를 예상해보세요", 0, 100, 50)

# 연애 팁 리스트
tips = {
    "썸 타는 중": [
        "너무 급하게 다가가지 마세요 😊",
        "상대의 말에 공감해주는 게 중요해요!",
        "가벼운 칭찬은 분위기를 좋게 만듭니다."
    ],
    "고백 고민 중": [
        "타이밍이 중요해요 💌",
        "직접 진심을 말하는 게 좋아요.",
        "결과보다 용기가 더 멋집니다!"
    ],
    "연락이 어렵다": [
        "짧고 가벼운 대화부터 시작하세요 📱",
        "상대의 관심사를 물어보세요.",
        "답장이 늦어도 너무 불안해하지 마세요."
    ],
    "데이트 준비 중": [
        "편안한 분위기의 장소가 좋아요 ☕",
        "상대 취향을 고려해보세요.",
        "너무 완벽하려고 하지 않아도 괜찮아요!"
    ]
}

# 버튼
if st.button("연애 조언 받기"):
    st.subheader(f"{name}님을 위한 조언 💡")

    # 랜덤 팁 출력
    advice = random.choice(tips[situation])
    st.success(advice)

    # 호감도 분석
    if interest >= 80:
        st.write("🔥 호감도가 꽤 높아 보여요!")
    elif interest >= 50:
        st.write("🙂 가능성이 있어요. 천천히 다가가보세요.")
    else:
        st.write("😅 조금 더 친해지는 시간이 필요해 보여요.")

    # 고민 출력
    if problem:
        st.info(f"입력한 고민: {problem}")

# 푸터
st.write("---")
st.caption("Made with ❤️ using Streamlit")
