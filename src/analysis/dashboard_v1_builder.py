from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


def build_dashboard_v1(season: SeasonConfig, weeks: list[DataKPIWeek]) -> dict:
    weeks_sorted = sorted(weeks, key=lambda w: w.season_week)

    if not weeks_sorted:
        raise ValueError("No hay datos semanales para generar dashboard")

    # Calculo los mesociclos
    # Para mi son cada 4 semanas
    # [TODO] No se si esto debe ser configurable, no creo trabajar con mesociclos diferentes a 4 semanas
    mesocycles = [{"week": w} for w in range(4, season.weeks + 1, 4)]

    # Configuración de los microciclos
    # Aquí si es importante manejar configuración semanal para kpis de cumplimiento y ver metas futuras
    microcycles = read_microcycles_config()

    current = weeks_sorted[-1]

    season_block = {
        "code": season.code,
        "season": season.season,
        "name": season.name,
        "start_date": season.start_date.isoformat(),
        "weeks": season.weeks,
        "year": season.start_date.year,
        "current_week": current.season_week,
        "week_start": current.week_start.isoformat(),
        "week_end": current.week_end.isoformat(),
    }

    weeks_block = [w.model_dump() for w in weeks_sorted]

    summary_cards = {
        "total_km": round(sum(w.distance_km for w in weeks_sorted), 2),
        "total_ascent_m": sum(w.ascent_m for w in weeks_sorted),
        "total_time_min": int(sum(w.time_min for w in weeks_sorted)),
        "total_sessions": sum(w.sessions for w in weeks_sorted),
    }

    # [TODO] Dejo el delta fuera, tengo que investigar bien como calcularlo y como
    # incluirlo en el dashboard y si me dice realmente algo
    weekly_series = (
        build_weekly_running_summary(weeks_sorted)
        .with_columns([
            pl.col("season_week").alias("week"),
            pl.col("distance_km").round(2).alias("km"),
            pl.lit(None).alias("delta_pct"),
        ])
        .select([
            "week",
            "week_start",
            "week_end",
            "km",
            "time_min",
            "ascent_m",
            "sessions",
            "delta_pct",
        ])
        .sort("week")
        .to_dicts()
    )

    weeks_strength = (
        build_weekly_strength_summary(weeks_sorted)
        .with_columns([
            pl.col("season_week").alias("week")
        ])
        .select([
            "week",
            "week_start",
            "week_end",
            "time_min",
            "sessions",
        ])
        .sort("week")
        .to_dicts()
    )

    weeks_min = build_combined_load_series(
        weekly_series,
        weeks_strength,
        season.weeks
    )

    return {
        "schema_version": "v1",
        "season": season_block,
        "weeks": weeks_block,
        "summary_cards": summary_cards,
        "weekly_series": weekly_series,
        "weekly_strength": weeks_strength,
        "weekly_min": weeks_min,
        "mesocycles": mesocycles,
        "microcycles": microcycles,
        "desafios": read_desafios_config(season.code),
    }

def read_microcycles_config() -> dict[int, dict[str, int | str]]:
    microcycles_config_path = Path("data/config/microcycles.json")
    if not microcycles_config_path.exists():
        return {}

    content = microcycles_config_path.read_text(encoding="utf-8")
    data = json.loads(content)

    r: dict[int, dict[str, int | str]] = {}

    for key, value in data.items():
        try:
            week_number = int(key.split(".")[1])   # key = T26.01
            r[week_number] = {
                "type": value.get("type"),
                "meta_km": value.get("meta_km"),
            }
        except (IndexError, ValueError):
            continue

    return r


def read_desafios_config(season_code: str) -> dict[int, dict]:
    path = Path("data/config/desafios.json")
    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))

    season_data = data.get(season_code, {})
    result = {}

    for key, value in season_data.items():
        try:
            week = int(key)
            result[week] = {
                "fecha": value.get("fecha"),
                "name": value.get("name"),
                "km": value.get("km"),
                "desnivel": value.get("desnivel"),
            }
        except ValueError:
            continue

    return result


def build_weekly_running_summary(weeks: list[DataKPIWeek]) -> pl.DataFrame:
    df = pl.DataFrame([w.model_dump() for w in weeks])

    # Dejo solamente las actividades de runing y trail
    # así evito problemas con otras actividades
    df_running = df.filter(
        pl.col("activity_type").is_in(["run", "trail"])
    )

    out = (
        df_running
        .group_by("season_week")
        .agg(
            pl.col("distance_km").sum().alias("distance_km"),
            pl.col("ascent_m").sum().alias("ascent_m"),
            pl.col("time_min").sum().alias("time_min"),
            pl.col("sessions").sum().alias("sessions"),
            pl.col("week_start").first(),
            pl.col("week_end").first(),
        )
        .sort("season_week")
    )

    return out


def build_weekly_strength_summary(weeks: list[DataKPIWeek]) -> pl.DataFrame:
    df = pl.DataFrame([w.model_dump() for w in weeks])

    df_gym = df.filter(
        pl.col("activity_type") == "gym"
    )

    out = (
        df_gym
        .group_by("season_week")
        .agg(
            pl.col("time_min").sum().alias("time_min"),
            pl.col("sessions").sum().alias("sessions"),
            pl.col("week_start").first(),
            pl.col("week_end").first(),
        )
        .sort("season_week")
    )

    return out

def build_combined_load_series(
    weekly_running: list[dict],
    weekly_strength: list[dict],
    total_weeks: int,
) -> list[dict]:

    running_dict = {w["week"]: w for w in weekly_running}
    strength_dict = {w["week"]: w for w in weekly_strength}

    out = []

    for week in range(1, total_weeks + 1):
        time_run = running_dict.get(week, {}).get("time_min", 0)
        time_gym = strength_dict.get(week, {}).get("time_min", 0)

        carga = time_run + (time_gym * 0.75)

        out.append({
            "week": week,
            "min": round(carga, 2),
        })

    return out
