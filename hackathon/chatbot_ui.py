"""
Hackathon: Banking Receptionist Chatbot — Streamlit UI

This file is COMPLETE. Do not modify it.
Build your agent logic in backend.py instead.

Run:
    streamlit run chatbot_ui.py
"""

import streamlit as st
from backend import handle_message

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Banking Assistant", page_icon="🏦", layout="centered")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Banking Assistant")
    st.markdown("---")
    st.markdown("**Sub-agents**")
    st.markdown("""
    - 💬 FAQ
    - 🏧 Account
    - 💸 Payments
    - 📦 Products
    - 📝 Complaints
    """)
    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown(
        "A receptionist (Haiku) classifies your intent, "
        "then routes to a specialist (Sonnet) with the right tools."
    )
    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("intent"):
            intent = msg["intent"]
            confidence = msg.get("confidence", 0)
            st.caption(f"🏷️ {intent}  •  confidence {confidence:.0%}")

# ---------------------------------------------------------------------------
# Handle user input
# ---------------------------------------------------------------------------
if user_input := st.chat_input("Ask me anything about banking..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = handle_message(user_input)

        # handle_message returns a dict with response, intent, confidence
        response = result.get("response", "Sorry, something went wrong.")
        intent = result.get("intent", "unknown")
        confidence = result.get("confidence", 0.0)

        st.markdown(response)
        if intent and intent != "none":
            st.caption(f"🏷️ {intent}  •  confidence {confidence:.0%}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "intent": intent,
        "confidence": confidence,
    })
