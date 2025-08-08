import time
import streamlit as st
from cognitive_substrate import Substrate

if 'input_queue' not in st.session_state:
    st.session_state.input_queue = []

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

if "aria_thoughts" not in st.session_state:
    st.session_state.aria_thoughts = []

state = 'active'
substrate = Substrate()
print("Aria is now active.")

# Streamlit UI
st.set_page_config(page_title="Aria", page_icon=":robot_face:", layout="wide")
st.title("Aria - Self-Guided AI")
st.write("Hello Alchemist.")
user_msg = st.text_area("Enter Message for Aria:", value=st.session_state.input_text)

if st.button("send"):
    if user_msg:
        st.session_state.input_queue.append(user_msg)
        st.session_state.input_text = ""

# Main loop that processes input
try:
    # Poll Signals | In the future call a function that aggregates signals          
    if st.session_state.input_queue:
        user_input = st.session_state.input_queue.pop(0)
        print(f"[User Input] {user_input}")
        response = substrate.process(user_input, st.session_state.aria_thoughts)
        print(f"\033[1;32mResponse: {response}\033[0m")
        for thought in st.session_state.aria_thoughts:
            st.write(f"**Thought:** {thought}")
            st.session_state.aria_thoughts = []
    else:
        print("[Aria] Generating ambient thought...Running core loop.")
        substrate.self_guide(st.session_state.aria_thoughts)
        for thought in st.session_state.aria_thoughts:
            st.write(f"**Thought:** {thought}")
            st.session_state.aria_thoughts = []
        # Run core loop             
    # Return response
except KeyboardInterrupt:
    # Handle Ctrl+C
    print("Interrupted. Exiting system...")