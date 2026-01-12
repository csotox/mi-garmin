from datetime import date

import polars as pl

from src.analysis.analysis import get_data_kpi_week_from_activity
from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


#-- - No voy a usar el fixture. Quiero que este código se mantenga constante
#-- - probablemente más adelante el fixture seasons.csv va a cambiar y no
#-- - quiero que afecte estas pruebas. Así que dejo el config fijo.
def get_season() -> SeasonConfig:
    return SeasonConfig(
        code="T2026",
        season=26,
        start_date=date(2025, 10, 13),
        weeks=40,
        name="Temporada 2026",
    )


def test_get_data_kpi_week_from_activity_basic():
    season = get_season()

    # Simulamos dos sesiones de entrenamiento
    data = {
        "start_time": [
            "2026-01-08 10:00:00",
            "2026-01-09 11:00:00",
        ],
        "sport": ["running", "running"],
        "total_distance": [5000.0, 7000.0],    # metros
        "total_timer_time": [1800.0, 2400.0],  # segundos
        "total_ascent": [100, 200],
        "total_descent": [90, 180],
        "avg_heart_rate": [140, 150],
        "max_heart_rate": [160, 170],
    }

    df = pl.DataFrame(data).with_columns(
        pl.col("start_time").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
    )

    result = get_data_kpi_week_from_activity(df, season)

    assert isinstance(result, list)

    # Validaciones
    week = result[0]
    assert isinstance(week, DataKPIWeek)
    assert week.sessions == 2
    assert week.distance_km == 12.0
    assert week.time_min == 70.0
    assert week.ascent_m == 300
    assert week.descent_m == 270
    assert week.avg_heart_rate == 145.0
    assert week.max_heart_rate == 170
