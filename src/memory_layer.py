from typing import Optional, Dict
import json
from .llm_client import LocalLLMClient
from .simple_memory import SimpleMemoryStore

class MemoryBackedLLM:
    """LLM with persistent conversation memory."""

    def __init__(self, llm_client: LocalLLMClient, mem_path: str = "mem_data/mem_store.jsonl"):
        self.llm = llm_client
        self.store = SimpleMemoryStore(mem_path)

    def chat(self, agent_id: str, user_id: str, system_prompt: str, 
             message: str, context_data: Optional[Dict] = None) -> str:

        # Get recent history
        history_chunks = self.store.get_recent(agent_id, user_id, k=5)
        history_text = "\n".join(history_chunks)

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        if history_text:
            messages.append({"role": "system", "content": f"Recent history:\n{history_text}"})

        if context_data:
            messages.append({"role": "system", "content": f"Current stats:\n{json.dumps(context_data, indent=2)}"})

        messages.append({"role": "user", "content": message})

        # Get response
        reply = self.llm.complete(messages)

        # Store interaction
        self.store.append(agent_id, user_id, f"User: {message}\nCoach: {reply}")

        return reply
