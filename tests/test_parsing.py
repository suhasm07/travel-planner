import json
from datetime import date

import pytest

from travel_planner.parsing import ParseError, parse_trip_request


class FakeLLM:
    def __init__(self, outputs: list[str]):
        self.outputs = outputs
        self.calls = 0

    def generate_json(self, system, prompt, schema):
        out = self.outputs[min(self.calls, len(self.outputs) - 1)]
        self.calls += 1
        return out


def test_valid_output_parsed():
    llm = FakeLLM([json.dumps({"destination": "Lisbon", "travelers": 2})])
    result = parse_trip_request("2 of us to Lisbon", llm, today=date(2026, 11, 14))
    assert result.destination == "Lisbon"
    assert result.travelers == 2


def test_repair_loop_recovers():
    bad = json.dumps({"destination": "Rome", "budget_total": -5})
    good = json.dumps({"destination": "Rome", "budget_total": 500})
    llm = FakeLLM([bad, good])
    result = parse_trip_request("Rome for $500", llm)
    assert result.budget_total == 500
    assert llm.calls == 2


def test_gives_up_after_max_repairs():
    llm = FakeLLM([json.dumps({"destination": "", "travelers": 0})])
    with pytest.raises(ParseError):
        parse_trip_request("???", llm, max_repairs=1)
