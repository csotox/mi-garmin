from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class DataKPIWeek(BaseModel):
    season: int = 0                    # Temporada de entrenamiento, ejemplo: 26 para 2026
    season_week: int = 0               # Número de semana dentro de la temporada
    season_code: str = ""              # Código de temporada, ejemplo: T26.10 para el año 2026 y semana 10
    activity_type: str = ""            # Tipo de actividad / ejercicio

    week_start: date                   # Fecha inicio de la semana
    week_end: date                     # Último entreno de la semana

    sessions: int = 0                  # Número de sesiones de entrenamiento
    distance_km: float = 0.0           # Distancia acumulada semanal
    time_min: float = 0.0              # Tiempo acumulado semanal

    ascent_m: int = 0                  # Running ascenso total
    descent_m: int = 0                 # Running descenso total (Se puede asumir que si subo debo bajar, pero la ruta puede ser diferente)

    avg_heart_rate: float = 0.0        # Pulso promedio de la sesión de entrenamiento
    max_heart_rate: int = 0            # Pulso máximo de la sesión de entrenamiento
