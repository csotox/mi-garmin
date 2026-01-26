from __future__ import annotations

from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


def build_dashboard_v1(season: SeasonConfig, weeks: list[DataKPIWeek]) -> dict:
    weeks_sorted = sorted(weeks, key=lambda w: w.season_week)

    if not weeks_sorted:
        raise ValueError("No hay datos semanales para generar dashboard")

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

    weekly_series = []
    prev_km = None

    for w in weeks_sorted:
        delta = None
        if prev_km and prev_km > 0:
            delta = round((w.distance_km - prev_km) / prev_km * 100, 1)

        weekly_series.append({
            "week": w.season_week,
            "week_start": w.week_start,
            "week_end": w.week_end,
            "km": round(w.distance_km, 2),
            "ascent_m": w.ascent_m,
            "sessions": w.sessions,
            "delta_pct": delta,
        })

        prev_km = w.distance_km

    microcycles = [{"week": w} for w in range(4, season.weeks + 1, 4)]

    return {
        "schema_version": "v1",
        "season": season_block,
        "weeks": weeks_block,
        "summary_cards": summary_cards,
        "weekly_series": weekly_series,
        "microcycles": microcycles,
    }
