import streamlit as st
from cognitive_substrate import Substrate

# Initialize or cache the Substrate instance
if 'substrate' not in st.session_state:
    st.session_state.substrate = Substrate()

substrate = st.session_state.substrate

st.title("Aria Interface")

# Mode Selection
mode = st.radio("Choose a mode:", ["Self-Guide Mode", "User Chat Mode"])

if mode == "Self-Guide Mode":
    st.subheader("Autonomous Thought Generation")
    if st.button("Run Self Guide"):
        with st.spinner("Thinking..."):
            result = substrate.self_guide()
            st.text_area("Generated Thought:", result, height=300)

elif mode == "User Chat Mode":
    st.subheader("Interactive Chat Interface")
    user_input = st.text_input("Enter your message:")
    if st.button("Submit"):
        with st.spinner("Processing input..."):
            response = substrate.process_input(user_input)
            st.markdown("**Aria's Response:**")
            st.text_area("Response:", response, height=300)

# Optional: Display current step or memory state for debugging
# st.write("Step:", substrate.step)
# st.write("Session Memory:", substrate.memory.session_memory)
# st.write("Context:", substrate.context)
