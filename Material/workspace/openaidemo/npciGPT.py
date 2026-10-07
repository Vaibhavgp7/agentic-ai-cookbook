import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
import uuid
import os
import json

THREADS_FILE = "chat_threads.json"

def load_threads():
    if os.path.exists(THREADS_FILE):
        with open(THREADS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def save_threads(threads):
    with open(THREADS_FILE, "w", encoding="utf-8") as f:
        json.dump(threads, f)


def add_thread(thread_id):
    threads = load_threads()
    threads.insert(0, {"id": thread_id, "label": f"Chat {thread_id[:8]}"})
    save_threads(threads)


@st.cache_resource
def get_agent():
    print("Getting agent...........it will take a while...........")
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)
    tools = [TavilySearch()]
    agent = create_agent(model=llm, tools=tools, checkpointer=InMemorySaver())

    return agent

agent = get_agent()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  
    add_thread(st.session_state.thread_id)


config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("NPCI GPT")
st.caption(f"Thread ID: {st.session_state.thread_id}")



snapshot= agent.get_state(config=config)



messages = snapshot.values.get("messages", [])
for message in messages:
    if (message.type == "human" or message.type == "ai") and message.content:
        with st.chat_message(message.type):
            st.markdown(message.content)


prompt= st.chat_input("Enter your message")
if prompt:
    agent.invoke(
        {
            "messages": [
                {"role": "user", "content": prompt}
            ],
           
        }, 
        config=config
    )
    st.rerun()

with st.sidebar:

    if st.button("New Thread"):
        st.session_state.thread_id = str(uuid.uuid4())
        add_thread(st.session_state.thread_id)
       
        st.rerun()
    threads = load_threads()

    ids = [thread["id"] for thread in threads]

    picked_thread_id = st.selectbox("Select a thread",
                            ids, 
                            index=ids.index(st.session_state.thread_id))

    if picked_thread_id != st.session_state.thread_id:
        st.session_state.thread_id = picked_thread_id
        
        st.rerun()





