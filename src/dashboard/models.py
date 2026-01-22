from datetime import date

from pydantic import BaseModel


class SeasonInfo(BaseModel):
    code: str
    season: int
    name: str
    start_date: date
    weeks: int


class KPIWeek(BaseModel):
    season: int
    season_week: int
    season_code: str
    week_start: date
    week_end: date
    sessions: int
    distance_km: float
    time_min: float
    ascent_m: int
    descent_m: int
    avg_heart_rate: float
    max_heart_rate: int


class DashboardDataV1(BaseModel):
    schema_version: str
    season: SeasonInfo
    generated_at: str
    weeks: list[KPIWeek]
