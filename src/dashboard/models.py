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
    week_start: date
    week_end: date
    ascent_m: int
    sessions: int
    time_min: float
    delta_pct: Optional[float]


class WeeklyMin(BaseModel):
    week: int
    min: float
    rolling_3: float
    pct_change: float
    is_overload: bool


class Mesocycle(BaseModel):
    week: int


class Microcycle(BaseModel):
    type: str
    meta_km: float


class Desafios(BaseModel):
    fecha: str
    name: str
    km: float
    desnivel: float


class DashboardSeason(BaseModel):
    code: str
    season: int
    name: str
    start_date: date
    weeks: int

    year: int | None = None
    current_week: int = 1               # No debe ser None nunca
    week_start: date | None = None
    week_end: date | None = None


class DashboardDataV1(BaseModel):
    schema_version: str
    season: DashboardSeason

    weeks: list[dict]

    summary_cards: SummaryCards
    weekly_series: list[WeeklySeries] = []
    weekly_min: list[WeeklyMin] = []
    mesocycles: list[Mesocycle] = []
    microcycles: dict[int, Microcycle] = {}
    desafios: dict[int, Desafios] = {}
