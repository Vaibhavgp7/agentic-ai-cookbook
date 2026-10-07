import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver
import uuid
import json
import os
load_dotenv()

CHECKPOINT_DB = "checkpoints.sqlite"

@st.cache_resource
def get_agent():
    conn = sqlite3.connect(CHECKPOINT_DB, check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)
    checkpointer.setup()  # create tables if needed

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tavily_tool = TavilySearch(
        max_results=3,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
        include_images=False,
    )

    return create_agent(
        model=model,
        tools=[tavily_tool],
        system_prompt=(
            "You are a helpful assistant with access to web search. "
            "Use web search when the user asks about current events, recent news, "
            "live data, or anything that needs up-to-date information from the internet. "
            "For personal facts the user told you earlier in the same chat, use memory — do not search the web."
        ),
        checkpointer=checkpointer,
    )

st.set_page_config(page_title="Memory Chatbot", layout="wide")
st.title("Chatbot with Memory")

agent = get_agent()
st.success("Agent ready. SqliteSaver + Tavily web search connected.")

# # --- Single-thread demo (fixed thread_id) ---
# THREAD_ID = "demo-thread-1"
# config = {"configurable": {"thread_id": THREAD_ID}}

# st.caption(f"Using thread: `{THREAD_ID}`")



# # --- One thread per browser session (unique id) ---
# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = str(uuid.uuid4())

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
    if any(t["id"] == thread_id for t in threads):
        return
    threads.insert(0, {"id": thread_id, "label": f"Chat {thread_id[:8]}"})
    save_threads(threads)

# Pick a thread when the app first opens
if "thread_id" not in st.session_state:
    threads = load_threads()
    if threads:
        st.session_state.thread_id = threads[0]["id"]
    else:
        st.session_state.thread_id = str(uuid.uuid4())
        add_thread(st.session_state.thread_id)

# --- Sidebar ---
with st.sidebar:
    st.header("Chats")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        add_thread(new_id)
        st.session_state.thread_id = new_id
        st.rerun()
    threads = load_threads()
    if threads:
        labels = [t["label"] for t in threads]
        ids = [t["id"] for t in threads]

        current_index = ids.index(st.session_state.thread_id)
        picked_label = st.selectbox(
            "Previous chats",
            labels,
            index=current_index,
        )
        picked_id = ids[labels.index(picked_label)]

        if picked_id != st.session_state.thread_id:
            st.session_state.thread_id = picked_id
            st.rerun()

    st.caption(f"Active thread:\n`{st.session_state.thread_id}`")

config = {"configurable": {"thread_id": st.session_state.thread_id}}
# st.caption(f"Thread ID: `{st.session_state.thread_id}`")

# Load existing messages from the checkpointer
snapshot = agent.get_state(config)
stored_messages = snapshot.values.get("messages", [])

# Show history
for msg in stored_messages:
    if msg.type == "human":
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif msg.type == "ai" and msg.content:
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# New user input
if prompt := st.chat_input("Say something..."):
    agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config,
    )
    st.rerun()



