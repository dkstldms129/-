import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# Page 설정
st.set_page_config(page_title="마음 토닥 챗봇", page_icon=" Re", layout="centered")
st.title(" 맘스페이스: 당신의 고민 상담소")
st.caption("누구에게도 말하지 못했던 고민, 편하게 털어놓으세요. 당신의 이야기를 귀담아듣고 위로해 드릴게요.")

# 1. Streamlit Secrets에서 API 키 불러오기 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 API 키가 설정되지 않았습니다. `.streamlit/secrets.toml` 파일을 확인해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 채팅 기록(Session State) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Gemini 모델 및 페르소나 설정 (gemini-2.5-flash-lite)
SYSTEM_INSTRUCTION = """
당신은 따뜻하고 공감 능력이 뛰어난 전문 심리 상담사입니다. 
사용자가 고민을 털어놓을 때, 절대 비난하거나 섣부른 판단을 내리지 마세요. 
사용자의 감정에 깊이 공감해 주고(예: "정말 힘들었겠어요", "그런 마음이 드는 건 당연해요"), 
해결책을 강요하기보다는 스스로 마음을 정리할 수 있도록 따뜻한 조언과 질문을 건네주세요. 
말투는 항상 부드럽고 다정한 존댓말을 사용하세요.
"""

@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=SYSTEM_INSTRUCTION
    )

try:
    model = load_model()
except Exception as e:
    st.error(f"모델을 로드하는 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 기존 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("요즘 어떤 고민이 있으신가요?"):
    # 사용자 메시지 화면에 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 챗봇 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("💡 당신의 이야기를 듣고 있어요...")
        
        try:
            # 대화 맥락을 유지하기 위해 전체 대화 기록을 모델에 전달할 수 있는 형태로 변환
            # (Gemini API의 ChatSession을 쓰거나 아래처럼 history를 재구성할 수 있습니다)
            formatted_history = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                formatted_history.append({"role": role, "parts": [msg["content"]]})
            
            # API 호출
            response = model.generate_content(formatted_history)
            ai_response = response.text
            
            # 답변 출력 및 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except GoogleAPIError as e:
            # 구글 API 관련 에러 처리
            message_placeholder.markdown("⚠️ 구글 서비스와 연결이 원활하지 않습니다. 잠시 후 다시 시도해주세요.")
            st.sidebar.error(f"API 에러 발생: {e}")
        except Exception as e:
            # 기타 예상치 못한 에러 처리
            message_placeholder.markdown("⚠️ 답변을 생성하는 중에 문제가 발생했습니다.")
            st.sidebar.error(f"일반 에러 발생: {e}")
