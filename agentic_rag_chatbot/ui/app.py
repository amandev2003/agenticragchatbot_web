# app.py

import sys, os

# 1) Calculate the path to the package root directory:
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)



import streamlit as st
from mcp.protocol import MCPRouter, MCPMessage

from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

import uuid

if "router" not in st.session_state:
    st.session_state.router = MCPRouter()
    st.session_state.ingestion_agent = IngestionAgent(st.session_state.router)
    st.session_state.retrieval_agent = RetrievalAgent(st.session_state.router)
    st.session_state.llm_response_agent = LLMResponseAgent(st.session_state.router)

    st.session_state.router.register("IngestionAgent", st.session_state.ingestion_agent.handle)
    st.session_state.router.register("RetrievalAgent", st.session_state.retrieval_agent.handle)
    st.session_state.router.register("LLMResponseAgent", st.session_state.llm_response_agent.handle)
    st.session_state.answer = None
    st.session_state.context = None

st.title("📄 Agentic RAG Chatbot ")
st.markdown("Upload documents, ask questions, and get answers based on the content.")

uploaded_files = st.file_uploader("Upload PDF, PPTX, DOCX, CSV, TXT files", type=["pdf", "pptx", "docx", "csv", "txt", "md"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Ingest Documents"):
        trace_id = str(uuid.uuid4())
        st.session_state["trace_id"] = trace_id

        msg = MCPMessage(
            sender="UI",
            receiver="IngestionAgent",
            type_="DOCUMENT_UPLOAD",
            payload={"files": uploaded_files, "trace_id": trace_id}
        )
        st.session_state.router.send(msg)
        st.success("Documents sent to IngestionAgent.")

st.divider()

query = st.text_input("🔍 Ask a question based on uploaded documents:")
if query and st.button("Get Answer"):
    trace_id = st.session_state.get("trace_id", str(uuid.uuid4()))

    query_msg = MCPMessage(
        sender="UI",
        receiver="RetrievalAgent",
        type_="USER_QUERY",
        payload={"query": query, "trace_id": trace_id}
    )
    st.session_state.router.send(query_msg)

# Handle final response from LLMResponseAgent (simulate MCP endpoint)
def handle_ui_response(message: MCPMessage):
    if message.type == "FINAL_ANSWER":
        st.session_state.answer = message.payload["answer"]
        st.session_state.context = message.payload["context"]

# Register UI as MCP recipient
st.session_state.router.register("UI", handle_ui_response)

if st.session_state.get("answer"):
    st.markdown("### ✅ Answer")
    st.success(st.session_state.answer)

if st.session_state.get("context"):
    with st.expander("📄 Source Context Chunks"):
        st.code(st.session_state.context)
