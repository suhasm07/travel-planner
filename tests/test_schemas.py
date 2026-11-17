from datetime import date, datetime

import pytest
from pydantic import ValidationError

from travel_planner.schemas import Activity, FlightOption, Stay, TripRequest


def test_end_date_computed_from_duration():
    t = TripRequest(destination="Lisbon", start_date=date(2027, 3, 1), duration_days=5)
    assert t.end_date == date(2027, 3, 5)


def test_duration_computed_from_dates():
    t = TripRequest(destination="Lisbon", start_date=date(2027, 3, 1), end_date=date(2027, 3, 7))
    assert t.duration_days == 7


def test_end_before_start_rejected():
    with pytest.raises(ValidationError):
        TripRequest(destination="Rome", start_date=date(2027, 3, 5), end_date=date(2027, 3, 1))


def test_negative_budget_rejected():
    with pytest.raises(ValidationError):
        TripRequest(destination="Rome", budget_total=-100)


def test_bad_currency_rejected():
    with pytest.raises(ValidationError):
        TripRequest(destination="Rome", currency="dollars")


def test_missing_optional_fields_ok():
    t = TripRequest(destination="Lisbon")
    assert t.budget_total is None
    assert t.interests == []
    assert t.travelers == 1


def test_empty_destination_rejected():
    with pytest.raises(ValidationError):
        TripRequest(destination="")


def test_too_many_travelers_rejected():
    with pytest.raises(ValidationError):
        TripRequest(destination="Rome", travelers=50)


def test_flight_arrival_before_departure_rejected():
    with pytest.raises(ValidationError):
        FlightOption(
            airline="X",
            origin="SYD",
            destination="LIS",
            departure=datetime(2027, 3, 2, 10, 0),
            arrival=datetime(2027, 3, 1, 10, 0),
            price=500,
            currency="USD",
        )


def test_invalid_latitude_rejected():
    with pytest.raises(ValidationError):
        Stay(name="Hotel", latitude=123, longitude=0, price_per_night=100, currency="USD")


def test_activity_defaults():
    a = Activity(name="Museum", category="museum", latitude=38.7, longitude=-9.1)
    assert a.estimated_cost == 0
    assert a.duration_minutes == 60
