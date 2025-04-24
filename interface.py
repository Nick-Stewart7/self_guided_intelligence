import streamlit as st
import json
import time
from cognitive_substrate import Substrate

# Initialize session state variables if they don't exist
if 'substrate' not in st.session_state:
    st.session_state.substrate = Substrate()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'show_thinking' not in st.session_state:
    st.session_state.show_thinking = False
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Conversation"
if 'system_logs' not in st.session_state:
    st.session_state.system_logs = []

def process_user_input():
    if st.session_state.user_input and not st.session_state.processing:
        user_message = st.session_state.user_input
        st.session_state.processing = True
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Clear the input box
        st.session_state.user_input = ""
        
        with st.spinner("Thinking..."):
            try:
                # Capture logs for detailed view
                log_capture = []
                
                # Process input based on selected mode
                if st.session_state.current_mode == "Conversation":
                    # Add a log entry
                    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Processing user input", "details": user_message}
                    st.session_state.system_logs.append(log_entry)
                    
                    # Process the input using the substrate
                    response = st.session_state.substrate.process_input(user_message)
                    
                    # Update step count from substrate
                    st.session_state.step_count = st.session_state.substrate.step
                    
                    # Add system response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Add response log
                    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Response generated", "details": "Length: " + str(len(response))}
                    st.session_state.system_logs.append(log_entry)
                    
                elif st.session_state.current_mode == "Self-Guided":
                    # Add a log entry
                    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Running self-guided mode"}
                    st.session_state.system_logs.append(log_entry)
                    
                    # Run self-guided mode
                    response = st.session_state.substrate.self_guide()
                    
                    # Add system response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Add response log
                    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Self-guided response generated", "details": "Length: " + str(len(response))}
                    st.session_state.system_logs.append(log_entry)
            
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.session_state.messages.append({"role": "system", "content": error_msg})
                log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Error occurred", "details": str(e)}
                st.session_state.system_logs.append(log_entry)
        
        st.session_state.processing = False

def toggle_thinking():
    st.session_state.show_thinking = not st.session_state.show_thinking

def change_mode(mode):
    st.session_state.current_mode = mode
    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Mode changed", "details": f"New mode: {mode}"}
    st.session_state.system_logs.append(log_entry)

def reset_conversation():
    st.session_state.messages = []
    st.session_state.substrate = Substrate()  # Reinitialize the substrate
    st.session_state.step_count = 0
    log_entry = {"time": time.strftime("%H:%M:%S"), "event": "Conversation reset"}
    st.session_state.system_logs.append(log_entry)

# Main App UI
st.title("AI Substrate System")

# Sidebar for controls and system state
with st.sidebar:
    st.header("Controls")
    
    # Mode selection
    st.subheader("Mode")
    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("Conversation", use_container_width=True, 
                    type="primary" if st.session_state.current_mode == "Conversation" else "secondary"):
            change_mode("Conversation")
    with mode_col2:
        if st.button("Self-Guided", use_container_width=True,
                    type="primary" if st.session_state.current_mode == "Self-Guided" else "secondary"):
            change_mode("Self-Guided")
    
    # System state visualization
    st.subheader("System State")
    st.metric("Step Count", st.session_state.step_count)
    st.metric("Memory Context Size", len(st.session_state.substrate.context))
    
    # Thinking process toggle
    st.checkbox("Show Thinking Process", value=st.session_state.show_thinking, on_change=toggle_thinking)
    
    # Reset button
    if st.button("Reset Conversation", type="secondary"):
        reset_conversation()
    
    # System information
    st.divider()
    st.caption("System Information")
    st.text(f"Current Mode: {st.session_state.current_mode}")
    st.text(f"Logs: {len(st.session_state.system_logs)} entries")

# Main chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Show thinking process if enabled
    if st.session_state.show_thinking and st.session_state.system_logs:
        with st.expander("Thinking Process", expanded=True):
            for log in st.session_state.system_logs[-5:]:  # Show last 5 logs
                st.text(f"[{log['time']}] {log['event']}")
                if 'details' in log:
                    st.text(f"  └─ {log['details']}")
            
            if len(st.session_state.system_logs) > 5:
                st.text(f"... and {len(st.session_state.system_logs) - 5} more logs")
                
            # Show current memory context summary
            st.subheader("Current Memory Context")
            st.text_area("Context", value=st.session_state.substrate.context, height=100, disabled=True)

# User input
user_input = st.chat_input("Enter your message", key="user_input", on_submit=process_user_input)

# Footer
st.divider()
st.caption("AI Substrate System - Prototype Interface")