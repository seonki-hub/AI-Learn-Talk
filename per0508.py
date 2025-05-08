import streamlit as st
import requests
import re

# 페이지 설정: 탭 로고(이모지)와 문구 변경
st.set_page_config(
    page_title="AI Learn Talk",
    page_icon="💬",  # 말풍선 이모지로 로고 변경
    layout="centered"
)

# 기본 API 키 설정 (임시 테스트용)
DEFAULT_API_KEY = "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"

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 사이드바 설정
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input(
    "Perplexity API 키",
    value=DEFAULT_API_KEY,
    type="password",
    help="기본 키가 설정되어 있지만 필요시 변경 가능합니다."
)
model = st.sidebar.selectbox("모델 선택", ["sonar-pro", "sonar-small"])

# 노란색 박스의 보안 주의사항 (한 줄 바꿈 적용)
st.sidebar.warning("**보안 주의사항**  \n프로그램은 데모용으로만 사용하세요.")

# 메인 인터페이스: 앱 상단 문구 변경
st.title("💬 AI Learn Talk")
st.caption("Perplexity API 기반 학습용 챗봇")

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("궁금한 것을 물어보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "너는 초등학생에게 친절하게 설명하는 선생님이야. "
        "쉬운 말과 예시를 써서 답변해줘. 반드시 한 문단(3~5문장)으로 간결하게 설명하고, "
        "절대 [1] 같은 각주나 출처 표시를 포함하지 마세요."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    try:
        with st.spinner("답변 생성 중..."):
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                bot_response = result['choices'][0]['message']['content']
                bot_response = re.sub(r'\[\d+\]', '', bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
            else:
                st.error(f"API 오류: {response.status_code}")
    except Exception as e:
        st.error(f"연결 오류: {str(e)}")
