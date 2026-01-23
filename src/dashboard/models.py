from datetime import date
from typing import Optional

from pydantic import BaseModel


class SeasonInfo(BaseModel):
    code: str
    name: str
    year: int
    current_week: int
    week_start: date
    week_end: date


class SummaryCards(BaseModel):
    total_km: float
    total_ascent_m: int
    total_time_min: int
    total_sessions: int


class WeeklySeries(BaseModel):
    week: int
    km: float
    ascent_m: int
    sessions: int
    delta_pct: Optional[float]


class Microcycle(BaseModel):
    week: int


class DashboardSeason(BaseModel):
    code: str
    season: int
    name: str
    start_date: date
    weeks: int

    year: int | None = None
    current_week: int | None = None
    week_start: date | None = None
    week_end: date | None = None


class DashboardDataV1(BaseModel):
    schema_version: str
    season: DashboardSeason

    weeks: list[dict]

    summary_cards: SummaryCards
    weekly_series: list[WeeklySeries] = []
    microcycles: list[Microcycle] = []
