# protocol.py
import uuid
from typing import Dict, Any

class MCPMessage:
    def __init__(self, sender: str, receiver: str, type_: str, payload: Dict[str, Any]):
        self.sender = sender
        self.receiver = receiver
        self.type = type_
        self.trace_id = str(uuid.uuid4())
        self.payload = payload

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "trace_id": self.trace_id,
            "payload": self.payload
        }

# Simple router for in-memory dispatching
class MCPRouter:
    def __init__(self):
        self.agents = {}

    def register(self, name: str, handler):
        self.agents[name] = handler

    def send(self, message: MCPMessage):
        receiver = message.receiver
        if receiver in self.agents:
            self.agents[receiver](message)
        else:
            print(f"Error: No agent registered with name '{receiver}'")
