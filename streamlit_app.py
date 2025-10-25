import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 챗봇나라")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 톤 선택 드롭다운
tone = st.selectbox("💡 챗봇 톤 선택:", ["정중한", "친근한", "유머러스한"])
tone_styles = {
    "정중한": {"color": "#A0C4FF", "emoji": "🎩"},
    "친근한": {"color": "#B5EAD7", "emoji": "😄"},
    "유머러스한": {"color": "#FFDAC1", "emoji": "😂"}
}

# 미리 입력 버튼 (빠른 질문 버튼)
st.markdown("### 🔘 빠른 질문")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("안녕하세요"):
        st.session_state.messages.append({"role": "user", "content": "안녕하세요"})
with col2:
    if st.button("오늘 날씨 알려줘"):
        st.session_state.messages.append({"role": "user", "content": "오늘 날씨 알려줘"})
with col3:
    if st.button("재밌는 농담 해줘"):
        st.session_state.messages.append({"role": "user", "content": "재밌는 농담 해줘"})


    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
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

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
