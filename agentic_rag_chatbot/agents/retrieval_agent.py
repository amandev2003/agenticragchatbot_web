# retrieval_agent.py
from mcp.protocol import MCPMessage, MCPRouter
from vector_store.faiss_index import VectorStore

class RetrievalAgent:
    def __init__(self, router: MCPRouter):
        self.router = router
        self.agent_name = "RetrievalAgent"
        self.vector_store = VectorStore()
        self.trace_store = {}  # trace_id → chunks

    def handle(self, message: MCPMessage):
        msg_type = message.type
        trace_id = message.payload.get("trace_id")

        if msg_type == "DOCUMENT_PARSED":
            self._handle_document_parsed(message, trace_id)

        elif msg_type == "USER_QUERY":
            self._handle_user_query(message, trace_id)

        else:
            print(f"[RetrievalAgent] Unknown message type: {msg_type}")

    def _handle_document_parsed(self, message: MCPMessage, trace_id: str):
        chunks = message.payload.get("chunks", [])
        filenames = message.payload.get("source_filenames", [])

        metadata_list = [{"file": fn} for fn in filenames for _ in range(len(chunks) // len(filenames))]

        self.vector_store.add_documents(chunks, metadata_list)

        # Store trace ID mapping (optional: useful for multi-user sessions)
        self.trace_store[trace_id] = {
            "chunks": chunks,
            "filenames": filenames
        }

        print(f"[RetrievalAgent] Stored {len(chunks)} chunks for trace ID: {trace_id}")

    def _handle_user_query(self, message: MCPMessage, trace_id: str):
        query = message.payload.get("query")
        if not query:
            print("[RetrievalAgent] Empty query received.")
            return

        top_results = self.vector_store.search(query, top_k=5)
        retrieved_chunks = [res["chunk"] for res in top_results]

        response = MCPMessage(
            sender=self.agent_name,
            receiver="LLMResponseAgent",
            type_="RETRIEVAL_RESULT",
            payload={
                "retrieved_chunks": retrieved_chunks,
                "query": query,
                "trace_id": trace_id
            }
        )
        self.router.send(response)
