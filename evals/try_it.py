from travel_planner.llm.gemini import GeminiClient
from travel_planner.parsing import parse_trip_request

llm = GeminiClient()
text = (
    "week in tokyo mid-april, 2 of us, around 3k, we love ramen and temples, no early mornings pls"
)
print(parse_trip_request(text, llm).model_dump_json(indent=2))
