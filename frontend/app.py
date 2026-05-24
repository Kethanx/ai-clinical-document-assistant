import uuid
import requests
import streamlit as st
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/questions/ask")

st.set_page_config(
    page_title="Cardiology Assistant",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Cardiology Assistant")
st.caption("Ask a question about heart failure, atrial fibrillation, or high blood pressure.")

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Session")
    st.write(f"Conversation ID: `{st.session_state.conversation_id}`")

    top_k = st.slider("Top K retrieved chunks", min_value=3, max_value=10, value=5)

    if st.button("New Conversation"):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("citations"):
            with st.expander("References"):
                for citation in message["citations"]:
                    pages = ", ".join(str(page) for page in citation["pages"])

                    st.markdown(f"**{citation['document_title']}**")
                    st.markdown(f"**Authors:** {citation['authors']}")
                    st.markdown(f"**Published:** {citation['publication_date']}")
                    st.markdown(f"**Pages:** {pages}")
                    st.divider()

user_question = st.chat_input("Ask your question...")

if user_question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    payload = {
        "question": user_question,
        "top_k": top_k,
        "conversation_id": st.session_state.conversation_id,
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=120)
                response.raise_for_status()
                data = response.json()

                answer = data["answer"]
                citations = data.get("citations", [])

                st.markdown(answer)

                if citations:
                    with st.expander("References"):
                        for citation in citations:
                            pages = ", ".join(str(page) for page in citation["pages"])

                            st.markdown(f"**{citation['document_title']}**")
                            st.markdown(f"**Authors:** {citation['authors']}")
                            st.markdown(f"**Published:** {citation['publication_date']}")
                            st.markdown(f"**Pages:** {pages}")
                            st.divider()

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "citations": citations,
                    }
                )

            except requests.exceptions.RequestException as e:
                error_message = f"Request failed: {e}"
                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "citations": [],
                    }
                )