from __future__ import annotations

import polars as pl

from src.analysis.activity_type import activity_type
from src.analysis.season_service import calculate_season_week
from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


#-- - Resumen semanal de sesiones de entrenamiento
#-- - Bases para calculo de kpis semanal
def get_data_kpi_week_from_activity(df_activity: pl.DataFrame, temporada:SeasonConfig) -> list[DataKPIWeek]:
    if df_activity.is_empty():
        return [DataKPIWeek()]

    #-- - Normalizamos unidades: distancia (m->km) y tiempo (s->min)
    df = df_activity.with_columns(
        (pl.col("total_distance") / 1000).alias("distance_km"),
        (pl.col("total_timer_time") / 60).alias("time_min"),
        pl.col("start_time").dt.date().alias("day"),
    )

    #-- - Asignamos los datos de la temporada
    #-- - Agregamos la columna season_week, para tener el número de la semana
    df = df.with_columns(
        pl.col("day")
        .map_elements(lambda d: calculate_season_week(d, temporada))
        .alias("season_week")
    )

    #-- - Asignamos el tipo de actividad
    df = df.with_columns(
        pl.col("sport")
        .map_elements(activity_type)
        .alias("activity_type")
)

    #-- - Agrupamos por semana y actividad
    # Agrupación semanal por fecha + tipo de actividad
    out = (
        df.group_by(["season_week", "activity_type"])
        .agg(
            pl.col("day").min().alias("week_start"),
            pl.col("day").max().alias("week_end"),
            pl.len().alias("sessions"),
            pl.col("distance_km").sum().alias("distance_km"),
            pl.col("time_min").sum().alias("time_min"),
            pl.col("total_ascent").sum().alias("ascent_m"),
            pl.col("total_descent").sum().alias("descent_m"),
            pl.col("avg_heart_rate").mean().alias("avg_heart_rate"),
            pl.col("max_heart_rate").max().alias("max_heart_rate"),
        )
        .sort("season_week")
    )

    print(out)

    return [DataKPIWeek(**row) for row in out.to_dicts()]
