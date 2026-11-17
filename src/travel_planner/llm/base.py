from typing import Protocol

from pydantic import BaseModel


class LLMClient(Protocol):
    def generate_json(self, system: str, prompt: str, schema: type[BaseModel]) -> str:
        """Return a JSON string conforming to `schema`."""
        ...
