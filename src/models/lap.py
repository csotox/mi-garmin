#-- - file: src/models/lap.py

from typing import Optional

from pydantic import BaseModel, Field


class LapSummary(BaseModel):
    lap_index: int = Field(..., ge=0)

    total_distance: float = Field(..., ge=0)
    total_timer_time: float = Field(..., gt=0)

    avg_heart_rate: Optional[int] = Field(None, gt=0)
    max_heart_rate: Optional[int] = Field(None, gt=0)

    total_ascent: Optional[int] = Field(None, ge=0)
    total_descent: Optional[int] = Field(None, ge=0)
