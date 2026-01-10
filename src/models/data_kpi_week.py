from __future__ import annotations

from pydantic import BaseModel


class DataKPIWeek(BaseModel):
    season: int | None = None          # Temporada de entrenamiento, ejemplo: 26 para 2026
    season_week: int | None = None     # Número de semana dentro de la temporada
    season_code: str | None = None     # Código de temporada, ejemplo: T26.10 para el año 2026 y semana 10

    week_start: str | None = None      # Fecha inicio de la semana
    week_end: str | None = None        # Último entreno de la semana

    sessions: int = 0                  # Número de sesiones de entrenamiento
    distance_km: float = 0.0           # Distancia acumulada semanal
    time_min: float = 0.0              # Tiempo acumulado semanal

    ascent_m: int = 0                  # Running ascenso total
    descent_m: int = 0                 # Running descenso total (Se puede asumir que si subo debo bajar, pero la ruta puede ser diferente)

    avg_heart_rate: float = 0.0        # Pulso promedio de la sesión de entrenamiento
    max_heart_rate: int = 0            # Pulso máximo de la sesión de entrenamiento
