# 🧠 Agentic RAG Chatbot for Multi-Format Document QA (MCP-Enabled)

This is an intelligent, agent-based Retrieval-Augmented Generation (RAG) chatbot that answers user queries from **uploaded documents** (PDF, DOCX, CSV, PPTX, TXT/Markdown). It uses a **multi-agent architecture** powered by a **Model Context Protocol (MCP)** to orchestrate tasks like document parsing, retrieval, and answer generation.

---

## 📌 Features

✅ Multi-format document parsing (PDF, PPTX, DOCX, CSV, TXT)  
✅ Agentic architecture with message-based coordination  
✅ Semantic retrieval via FAISS + sentence-transformers  
✅ Response generation via local LLMs (Falcon-RW-1B or any compatible HuggingFace model)  
✅ Fully offline capable (no OpenAI API required)  
✅ Streamlit-powered UI with multi-turn chat support  
✅ Traceable and explainable answers with source chunks

---

## 🏗️ Architecture Overview

This project follows a modular, agent-based architecture with clearly defined agents:

### 🧩 Agents

| Agent              | Role                                                                 |
|-------------------|----------------------------------------------------------------------|
| `IngestionAgent`   | Parses and preprocesses uploaded documents                           |
| `RetrievalAgent`   | Embeds content, performs semantic search using FAISS                 |
| `LLMResponseAgent` | Forms LLM prompt using top-k results and generates natural responses |

### 🔁 Message Passing via MCP

All agents communicate using an internal messaging protocol resembling:

```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "CONTEXT_RESPONSE",
  "trace_id": "rag-457",
  "payload": {
    "top_chunks": ["..."],
    "query": "What KPIs were tracked in Q1?"
  }
}


📁 Project Structure
agentic_rag_chatbot/
│
├── agents/
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   └── llm_response_agent.py
│
├── vector_store/
│   └── faiss_index.py
│
├── utils/
│   └── parsers.py
│
├── mcp/
│   └── protocol.py
│
├── ui/
│   └── app.py
│
├── main.py
├── requirements.txt
└── README.md
