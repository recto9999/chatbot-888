import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 챗봇나라")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# === 세션 상태 초기화 ===
# 메인 채팅 메시지 리스트 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# MBTI/혈액형용 커스텀 메시지 리스트 초기화 (이 부분이 누락되었습니다)
if "custom_messages" not in st.session_state:
    st.session_state.custom_messages = []
# ========================


# Ask user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # --- MBTI 및 혈액형 입력 섹션 ---
    mbti_options = ["INTJ", "INTP", "ENTJ", "ENTP",
                    "INFJ", "INFP", "ENFJ", "ENFP",
                    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                    "ISTP", "ISFP", "ESTP", "ESFP"]
    mbti = st.selectbox("💡 MBTI 선택:", mbti_options)

    blood_options = ["A", "B", "AB", "O"]
    blood_type = st.selectbox("💡 혈액형 선택:", blood_options)

    # "제출" 버튼 로직 수정
    if st.button("제출"):
        user_input = f"내 MBTI는 {mbti}이고, 혈액형은 {blood_type}이야."
        
        # 1. custom_messages에 사용자 입력 추가
        st.session_state.custom_messages.append({"role": "user", "content": user_input})

        # 2. 불필요한 last_msg 확인 로직 제거
        # 3. API 호출 (custom_messages만 사용)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.custom_messages # 'messages'와 섞지 않음
        )
        
        # 4. API 응답 파싱 오류 수정 (.content 사용)
        bot_message = response.choices[0].message.content
        
        # 5. custom_messages에 봇 응답 추가
        st.session_state.custom_messages.append({"role": "assistant", "content": bot_message})

    # "custom_messages" 출력 (이 로직은 문제 없었음)
    if st.session_state.custom_messages: # 'in' 검사 대신 리스트가 비어있지 않은지 확인
        st.markdown("### 💬 MBTI/혈액형 입력 대화")
        for msg in st.session_state.custom_messages:
            if msg["role"] == "user":
                st.markdown(f"**🙂 사용자:** {msg['content']}")
            else:
                st.markdown(f"**🤖 챗봇:** {msg['content']}")
        st.divider() # 구분을 위한 라인 추가

    # --- 메인 채팅 섹션 ---
    
    # Display the existing chat messages via `st.chat_message`.
    st.markdown("### 💬 메인 챗봇")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
