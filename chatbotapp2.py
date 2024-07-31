import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Streaming Chat-GPT-like Clone 👽")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the initial sign if there are no messages
if not st.session_state.messages:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 50vh;">
            <h1 style="background: linear-gradient(to right, #ff6ec4, #7873f5); -webkit-background-clip: text; color: transparent; font-size: 3em;">
                Start writing a prompt...
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for new messages
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = ""
        for chunk in stream:
            response += chunk['choices'][0]['delta'].get('content', '')
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
