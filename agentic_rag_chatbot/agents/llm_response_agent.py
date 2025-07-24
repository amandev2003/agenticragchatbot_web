from mcp.protocol import MCPMessage, MCPRouter
import openai

class LLMResponseAgent:
    def __init__(self, router: MCPRouter):
        self.router = router
        self.agent_name = "LLMResponseAgent"

    def handle(self, message: MCPMessage):
        msg_type = message.type
        if msg_type != "RETRIEVAL_RESULT":
            print(f"[LLMResponseAgent] Unsupported message type: {msg_type}")
            return

        payload = message.payload
        query = payload.get("query")
        chunks = payload.get("retrieved_chunks", [])
        trace_id = payload.get("trace_id")

        if not query or not chunks:
            print("[LLMResponseAgent] Empty query or context. Skipping.")
            return

        context_str = "\n\n".join([f"- {chunk}" for chunk in chunks])
        prompt = f"""You are an intelligent assistant helping users answer questions based on provided document excerpts.

Context:
{context_str}

Question:
{query}

Answer:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant answering questions based on context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[LLMResponseAgent] LLM Error: {e}")
            answer = "Sorry, I encountered an error while generating the response."

        final_message = MCPMessage(
            sender=self.agent_name,
            receiver="UI",
            type_="FINAL_ANSWER",
            payload={
                "answer": answer,
                "context": context_str,
                "query": query,
                "trace_id": trace_id
            }
        )
        self.router.send(final_message)
