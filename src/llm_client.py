from dataclasses import dataclass
from typing import List, Dict
import requests
import os

@dataclass
class LLMConfig:
    base_url: str
    model: str
    timeout: int = 60
    temperature: float = 0.3

class LocalLLMClient:
    """OpenAI-compatible client for local LLMs."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def complete(self, messages: List[Dict[str, str]]) -> str:
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": 1024,
        }

        try:
            resp = requests.post(self.config.base_url, json=payload, timeout=self.config.timeout)
            resp.raise_for_status()
            data = resp.json()

            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            elif "response" in data:
                return data["response"]
            else:
                raise ValueError(f"Unexpected response: {data}")
        except requests.exceptions.RequestException as e:
            return f"[LLM Error: {str(e)}]"

def get_llm_config() -> LLMConfig:
    return LLMConfig(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1/chat/completions"),
        model=os.getenv("LLM_MODEL", "mistral:7b-instruct"),
    )
