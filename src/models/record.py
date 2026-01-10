from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RecordPoint(BaseModel):
    timestamp: datetime

    heart_rate: Optional[int] = Field(None, gt=0)
    speed: Optional[float] = Field(None, ge=0)
    altitude: Optional[float] = None
