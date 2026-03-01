from __future__ import annotations

import polars as pl

from src.analysis.activity_type import activity_type
from src.analysis.season_service import build_season_code, calculate_season_week, get_season_week_range
from src.analysis.transform import load_overrides
from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


#-- - Resumen semanal de sesiones de entrenamiento
#-- - Bases para calculo de kpis semanal
def get_data_kpi_week(
        df_activity: pl.DataFrame,
        df_records: pl.DataFrame,
        temporada:SeasonConfig
) -> tuple[list[DataKPIWeek], pl.DataFrame]:

    if df_activity.is_empty():
        return [], pl.DataFrame()

    #-- - Normalizamos unidades: distancia (m->km) y tiempo (s->min)
    df = df_activity.with_columns(
        (pl.col("total_distance") / 1000).alias("distance_km"),
        (pl.col("total_timer_time") / 60).alias("time_min"),
        pl.col("start_time").dt.date().alias("day"),
    )

    #-- - Asignamos los datos de la temporada
    #-- - Agregamos la columna season_week, para tener el número de la semana
    #-- - Asignamos el tipo de actividad
    df = df.with_columns(
        pl.col("day")
        .map_elements(lambda d: calculate_season_week(d, temporada))
        .alias("season_week"),
        pl.col("sport")
        .map_elements(activity_type)
        .alias("activity_type"),
    )

    #-- - Calculo datos de la frecuencia cardiaca
    df = _calc_fc(df, df_records)

    #-- - Reclasificar algunas actividades según necesidad
    #-- - Ej.: run -> trail
    overrides = load_overrides()

    if overrides:
        over_aux = pl.DataFrame({
            "file_name": list(overrides.keys()),
            "override_type": list(overrides.values())
        })

        df = df.join(over_aux, on="file_name", how="left")

        df = df.with_columns(
            pl.coalesce(
                pl.col("override_type"),
                pl.col("activity_type")
            ).alias("activity_type")
        ).drop("override_type")


    #-- - Agrupamos por semana y actividad
    #-- - Agrupación semanal por fecha + tipo de actividad
    out_temp = (
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
        .sort(["season_week", "activity_type"])
    )

    out = []

    for row in out_temp.to_dicts():
        week = row["season_week"]

        week_start, week_end = get_season_week_range(temporada, week)

        out.append(
            DataKPIWeek(
                season=temporada.season,
                season_week=week,
                season_code=build_season_code(temporada, week),
                week_start=week_start,
                week_end=week_end,
                sessions=row["sessions"],
                activity_type=row["activity_type"],
                distance_km=round(row["distance_km"], 2),
                time_min=round(row["time_min"], 2),
                ascent_m=row["ascent_m"],
                descent_m=row["descent_m"],
                avg_heart_rate=round(row["avg_heart_rate"], 2),
                max_heart_rate=row["max_heart_rate"],
            )
        )

    return out, df

#-- -
#-- - Agregas dos columnas a cada fila del df
#-- - La media de la frecuencia cardiaca en la primera y seguda hora
def _calc_fc(df, df_records):
    if df_records.is_empty():
        return df

    df_records_sorted = df_records.sort(["activity_id", "timestamp"])

    mitad = (
        df_records_sorted
        .with_columns(
            pl.arange(0, pl.count()).over("activity_id").alias("idx"),
            pl.col("timestamp").count().over("activity_id").alias("total_points")
        )
        .with_columns(
            (pl.col("idx") < (pl.col("total_points") / 2)).alias("first_half")
        )
        .group_by(["activity_id", "first_half"])
        .agg(
            pl.col("heart_rate").mean().alias("avg_hr_half")
        )
        .pivot(
            index="activity_id",
            columns="first_half",
            values="avg_hr_half"
        )
        .rename({
            "true": "avg_hr_first_half",
            "false": "avg_hr_second_half"
        })
    )

    df = df.join(mitad, on="activity_id", how="left")

    return df
