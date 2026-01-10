from __future__ import annotations

from datetime import date

import polars as pl

from src.models.data_kpi_week import DataKPIWeek


#-- - Resumen semanal de sesiones de entrenamiento
#-- - Bases para calculo de kpis semanal
#-- - [TODO]
#-- -   -[X] ¿La estructura de datos devuelta puede ser tipada como los models de typescript?
#-- -   -[X] Crear utils.py (Restuesta) No es necesario porque polars es vectorizado y si uso utils se rompe la vectorización
#-- -   -[X] Diferenciar tipo de actividad (correr, caminar, gimnasio, etc.)
#-- -   -[ ] Establecer semanas
def get_data_kpi_week_from_activity(df_activity: pl.DataFrame) -> DataKPIWeek:
    if df_activity.is_empty():
        return DataKPIWeek()

    #-- - Normalizamos unidades: distancia (m->km) y tiempo (s->min)
    df = df_activity.with_columns(
        (pl.col("total_distance") / 1000).alias("distance_km"),
        (pl.col("total_timer_time") / 60).alias("time_min"),
        pl.col("start_time").dt.date().alias("day"),
    )

    #-- - Calculo de rango de fecha de la semana
    min_day = df.select(pl.col("day").min()).item()
    max_day = df.select(pl.col("day").max()).item()

    out = {
        "week_start": str(min_day) if isinstance(min_day, date) else None,
        "week_end": str(max_day) if isinstance(max_day, date) else None,
        "sessions": int(df.height),
        "distance_km": float(df.select(pl.col("distance_km").sum()).item() or 0.0),
        "time_min": float(df.select(pl.col("time_min").sum()).item() or 0.0),
        "ascent_m": int(df.select(pl.col("total_ascent").sum()).item() or 0),
        "descent_m": int(df.select(pl.col("total_descent").sum()).item() or 0),
    }

    if "avg_heart_rate" in df.columns:
        out["avg_heart_rate"] = float(df.select(pl.col("avg_heart_rate").mean()).item() or 0.0)
    if "max_heart_rate" in df.columns:
        out["max_heart_rate"] = int(df.select(pl.col("max_heart_rate").max()).item() or 0)

    return DataKPIWeek(**out)
