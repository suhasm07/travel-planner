from __future__ import annotations

import datetime as dt
from datetime import date, datetime, timedelta
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class TravelStyle(StrEnum):
    BUDGET = "budget"
    MIDRANGE = "midrange"
    LUXURY = "luxury"


class TripRequest(BaseModel):
    """Structured form of what the user asked for."""

    destination: str = Field(min_length=1, description="City or region to visit")
    origin: str | None = Field(default=None, description="Departure city, if stated")
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=30)
    travelers: int = Field(default=1, ge=1, le=12)
    budget_total: float | None = Field(default=None, gt=0, description="Total budget for the trip")
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    interests: list[str] = Field(default_factory=list)
    travel_style: TravelStyle | None = None
    constraints: list[str] = Field(
        default_factory=list, description="e.g. 'vegetarian', 'no early mornings'"
    )
    missing_info: list[str] = Field(
        default_factory=list, description="Important details the user did not provide"
    )

    @model_validator(mode="after")
    def reconcile_dates(self) -> TripRequest:
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be on or after start_date")
            self.duration_days = (self.end_date - self.start_date).days + 1
        elif self.start_date and self.duration_days:
            self.end_date = self.start_date + timedelta(days=self.duration_days - 1)
        return self


class FlightOption(BaseModel):
    airline: str
    origin: str
    destination: str
    departure: datetime
    arrival: datetime
    price: float = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    stops: int = Field(default=0, ge=0)
    booking_url: str | None = None

    @model_validator(mode="after")
    def arrival_after_departure(self) -> FlightOption:
        if self.arrival <= self.departure:
            raise ValueError("arrival must be after departure")
        return self


class Stay(BaseModel):
    name: str
    area: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    price_per_night: float = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    rating: float | None = Field(default=None, ge=0, le=5)
    source: str | None = None


class Activity(BaseModel):
    name: str
    category: str  # e.g. "museum", "restaurant", "park"
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    estimated_cost: float = Field(default=0, ge=0)
    duration_minutes: int = Field(default=60, ge=5, le=720)
    description: str | None = None
    source: str | None = None


class DayPlan(BaseModel):
    day_number: int = Field(ge=1)
    date: dt.date | None = None
    activities: list[Activity]
    notes: str | None = None


class Itinerary(BaseModel):
    request: TripRequest
    flight: FlightOption | None = None
    stay: Stay | None = None
    days: list[DayPlan]
    total_estimated_cost: float = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    summary: str | None = None
