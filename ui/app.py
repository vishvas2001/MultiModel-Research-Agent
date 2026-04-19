import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Private-Pulse Agent", layout="wide", initial_sidebar_state="expanded")

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# --- Callback for the Cancel Button ---
def cancel_generation():
    """This runs instantly when the Stop button is clicked, interrupting the stream."""
    st.session_state.is_processing = False
    st.session_state.messages.append({"role": "assistant", "content": "🚫 *Generation cancelled by user.*"})

# --- Sidebar ---
with st.sidebar:
    st.header("📄 Knowledge Base")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], disabled=st.session_state.is_processing)
    
    if uploaded_file:
        if st.button("Index Document", use_container_width=True, disabled=st.session_state.is_processing):
            with st.spinner("Chunking & embedding..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                res = requests.post(f"{API_URL}/api/upload", files=files)
                if res.status_code == 200:
                    st.success("Indexed successfully!")
                else:
                    st.error("Failed to index.")

st.title("🧠 Private-Pulse Research Agent")

# --- Render Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Placeholder for the Cancel Button ---
# We define it here so it appears above the active chat block
cancel_container = st.empty()

# --- User Input ---
prompt = st.chat_input("Ask the research agent...", disabled=st.session_state.is_processing)

if prompt:
    # 1. Add user prompt to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Lock the UI and show the Cancel Button
    st.session_state.is_processing = True
    with cancel_container:
        st.button("🛑 Cancel Generation", on_click=cancel_generation, key="cancel_btn")

    # 3. Generate Assistant Response
    with st.chat_message("assistant"):
        status = st.status("🕵️‍♂️ Agent is thinking...", expanded=True)
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with requests.post(
                f"{API_URL}/api/chat/stream", 
                json={"query": prompt, "session_id": "session_1"}, 
                stream=True,
                timeout=300 
            ) as response:
                
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line.replace("data: ", "")
                            event = json.loads(data_str)
                            
                            if event["type"] == "token":
                                full_response += event["content"]
                                message_placeholder.markdown(full_response + "▌")
                                
                            elif event["type"] == "log":
                                status.markdown(f"- {event['content']}")
                                
                            elif event["type"] == "error":
                                status.error(f"Error: {event['content']}")
            
            status.update(label="Research Complete!", state="complete", expanded=False)
            
            # Save the final text output only if it wasn't cancelled
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            
        except Exception as e:
            # If the user clicks cancel, Streamlit interrupts the loop. 
            # We don't want to show an ugly error, so we pass.
            pass
        
    # 4. Clean up the UI, hide the cancel button, and unlock the text input
    cancel_container.empty()
    st.session_state.is_processing = False
    st.rerun()