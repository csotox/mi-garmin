from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ActivitySummary(BaseModel):
    start_time: datetime    # Fecha/hora inicio de la actividad
    sport: str              # Tipo de actividad

    total_distance: float = Field(..., gt=0, description="Distancia total en metros")
    total_timer_time: float = Field(..., gt=0, description="Tiempo activo en segundos")

    avg_heart_rate: Optional[int] = Field(None, gt=0)   # Pulso promedio
    max_heart_rate: Optional[int] = Field(None, gt=0)   # Pulso maximo durante la actividad

    total_ascent: Optional[int] = Field(None, ge=0)     # Mts desnivel positivo
    total_descent: Optional[int] = Field(None, ge=0)    # Mts desnivel negativo
