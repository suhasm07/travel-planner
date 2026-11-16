from google import genai

from travel_planner.config import settings

client = genai.Client(api_key=settings.gemini_api_key)
response = client.models.generate_content(model=settings.gemini_model, contents="Say hi in 3 words")
print(response.text)
