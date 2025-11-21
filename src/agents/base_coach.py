from typing import Optional, Dict
from ..memory_layer import MemoryBackedLLM

class BaseCoach:
    agent_id: str = "generic"

    def __init__(self, mem_llm: MemoryBackedLLM, system_prompt: str):
        self.mem_llm = mem_llm
        self.system_prompt = system_prompt

    def chat(self, user_id: str, message: str, context_data: Optional[Dict] = None) -> str:
        return self.mem_llm.chat(self.agent_id, user_id, self.system_prompt, message, context_data)
