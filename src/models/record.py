from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models import activity


class RecordPoint(BaseModel):
    activity_id: str
    timestamp: datetime

    heart_rate: Optional[int] = Field(None, gt=0)
    speed: Optional[float] = Field(None, ge=0)
    altitude: Optional[float] = None
