import streamlit as st
import requests

st.set_page_config(page_title="Calendar AI Chat", page_icon="📅")

st.title("📅 Calendar AI Assistant")
st.markdown("Talk to your calendar using natural language (e.g., 'Book meeting tomorrow at 4 PM')")

# 🔹 1. Initialize chat history (once)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔹 2. Chat Input Area
user_input = st.chat_input("Type your message...")

# 🔹 3. On message submit
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Call the backend
    with st.spinner("💬 Talking to Calendar Agent..."):
        try:
            res = requests.post("http://localhost:8000/agent", json={"message": user_input})
            if res.status_code == 200:
                agent_response = res.json()["response"]["output"]
                # Append agent response
                st.session_state.chat_history.append({"role": "agent", "content": str(agent_response)})
            else:
                st.session_state.chat_history.append({
                    "role": "agent",
                    "content": f"❌ API Error: {res.status_code}"
                })
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "agent",
                "content": f"💥 Backend Error: {e}"
            })

# 🔹 4. Display Chat History
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])
