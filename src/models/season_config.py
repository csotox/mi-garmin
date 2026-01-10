from datetime import date

from pydantic import BaseModel


class SeasonConfig(BaseModel):
    code: str = ""                         # Código de la temporada | T2026
    season: int = 0                        # Número de la temporada | 26
    start_date: date = date(2026, 1, 1)    # Fecha de inicio | 2025-10-13
    weeks: int = 0                         # Número de semanas de duración | 40
    name: str = ""                         # Nombre | Temporada 2026

class SeasonConfigList(BaseModel):
    seasons: list[SeasonConfig]
