from google import genai
from google.genai import types
from pydantic import BaseModel

from travel_planner.config import settings


class GeminiClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self._client = genai.Client(api_key=api_key or settings.gemini_api_key)
        self._model = model or settings.gemini_model

    def generate_json(self, system: str, prompt: str, schema: type[BaseModel]) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0,
            ),
        )
        return response.text
