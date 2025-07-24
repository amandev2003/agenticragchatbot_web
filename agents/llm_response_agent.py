from mcp.protocol import MCPMessage
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os
from pathlib import Path
import torch
class LLMResponseAgent:
    def __init__(self, router):
        self.router = router
        self.agent_name = "LLMResponseAgent"

        model_id = "tiiuae/falcon-rw-1b"

        # Load model and tokenizer safely
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=None  # Don't use 'auto' here
        )

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )



    def handle(self, message: MCPMessage):
        if message.type != "RETRIEVAL_RESULT":
            print(f"[LLMResponseAgent] Unsupported message type: {message.type}")
            return

        context = "\n".join(message.payload["retrieved_chunks"])
        query = message.payload["query"]
        trace_id = message.payload["trace_id"]

        prompt = f"Answer the following question based only on the given context.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

        try:
            response = self.generator(prompt, max_new_tokens=200, do_sample=False)
            answer = response[0]["generated_text"].split("Answer:")[-1].strip()
        except Exception as e:
            answer = f"Error generating answer: {e}"

        self.router.send(MCPMessage(
            sender=self.agent_name,
            receiver="UI",
            type_="FINAL_ANSWER",
            payload={
                "answer": answer,
                "context": context,
                "query": query,
                "trace_id": trace_id
            }
        ))
