import streamlit as st

st.set_page_config(page_title="Echo Chat", layout="wide")
st.title("Echo Chat (no AI — just Streamlit UI practice)")

with st.sidebar:
    st.header("Sidebar")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Remember messages between reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Read new input from the user
if prompt := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": f"You said: {prompt}"})
    st.rerun()