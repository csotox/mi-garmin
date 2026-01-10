import polars as pl

from src.analysis.analysis import get_data_kpi_week_from_activity
from src.models.data_kpi_week import DataKPIWeek


def test_get_data_kpi_week_from_activity_basic():
    # Simulamos dos sesiones de entrenamiento
    data = {
        "start_time": [
            "2026-01-08 10:00:00",
            "2026-01-09 11:00:00",
        ],
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

    result = get_data_kpi_week_from_activity(df)

    assert isinstance(result, DataKPIWeek)

    # Validaciones
    assert result.sessions == 2
    assert result.distance_km == 12.0
    assert result.time_min == 70.0
    assert result.ascent_m == 300
    assert result.descent_m == 270
    assert result.avg_heart_rate == 145.0
    assert result.max_heart_rate == 170
