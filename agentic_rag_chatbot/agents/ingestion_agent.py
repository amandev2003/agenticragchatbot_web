from mcp.protocol import MCPMessage, MCPRouter
from utils.parsers import parse_file
import uuid

class IngestionAgent:
    def __init__(self, router: MCPRouter):
        self.router = router
        self.agent_name = "IngestionAgent"

    def handle(self, message: MCPMessage):
        """
        This agent only responds to document ingestion requests.
        Expected message.payload: {"files": [UploadedFile1, UploadedFile2], "trace_id": "..."}
        """
        trace_id = message.payload.get("trace_id", str(uuid.uuid4()))
        files = message.payload.get("files", [])
        all_chunks = []
        source_filenames = []

        for file in files:
            try:
                chunks = parse_file(file)
                tagged_chunks = [f"{file.name}: {chunk}" for chunk in chunks]
                all_chunks.extend(tagged_chunks)
                source_filenames.append(file.name)
            except Exception as e:
                print(f"[IngestionAgent] Failed to parse {file.name}: {e}")

        if not all_chunks:
            print("[IngestionAgent] No chunks parsed. Aborting.")
            return

        # Create and send MCP message to RetrievalAgent
        response = MCPMessage(
            sender=self.agent_name,
            receiver="RetrievalAgent",
            type_="DOCUMENT_PARSED",
            payload={
                "chunks": all_chunks,
                "source_filenames": source_filenames,
                "trace_id": trace_id
            }
        )
        self.router.send(response)
