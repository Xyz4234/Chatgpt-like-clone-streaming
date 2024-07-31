import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Streaming Chat-GPT-Like Clone 😘")

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CSS to style the input prompt
st.markdown("""
    <style>
    .prompt-box {
        position: relative;
    }
    .prompt-placeholder {
        position: absolute;
        top: 0;
        left: 0;
        padding: 10px;
        color: white;
        background: linear-gradient(45deg, red, purple);
        border-radius: 5px;
        z-index: 1;
        transition: opacity 0.2s ease-out;
    }
    .prompt-box input:focus + .prompt-placeholder,
    .prompt-box input:not(:placeholder-shown) + .prompt-placeholder {
        opacity: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Create a container for the input prompt
prompt_container = st.container()

# Add the input prompt with a colorful placeholder
with prompt_container:
    st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
    prompt = st.text_input("", key="input_prompt", placeholder="Start writing in prompt")
    st.markdown('<div class="prompt-placeholder">Start writing in prompt</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if prompt:
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
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
