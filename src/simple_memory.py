import json
from pathlib import Path
from typing import List, Dict

class SimpleMemoryStore:
    """Ultra-simple persistent memory using JSONL."""

    def __init__(self, path: str = "mem_store.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("")

    def append(self, agent_id: str, user_id: str, content: str):
        record = {"agent_id": agent_id, "user_id": user_id, "content": content}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def get_recent(self, agent_id: str, user_id: str, k: int = 5) -> List[str]:
        if not self.path.exists():
            return []

        lines = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        filtered = [
            rec["content"] for rec in lines
            if rec.get("agent_id") == agent_id and rec.get("user_id") == user_id
        ]
        return filtered[-k:]
