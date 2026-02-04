from __future__ import annotations

import json
from pathlib import Path

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

    weekly_series = []
    # prev_km = None

    for w in weeks_sorted:
        # [TODO] Dejo el delta fuera, tengo que investigar bien como calcularlo y como
        # incluirlo en el dashboard y si me dice realmente algo
        delta = None
        # week_type = None
        # if w.season_week in microcycles:
        #     week_type = microcycles[w.season_week]["type"]

        # if week_type != "descarga":
        #     if prev_km and prev_km > 0:
        #         delta = round((w.distance_km - prev_km) / prev_km * 100, 1)

        #     prev_km = w.distance_km

        weekly_series.append({
            "week": w.season_week,
            "week_start": w.week_start,
            "week_end": w.week_end,
            "km": round(w.distance_km, 2),
            "ascent_m": w.ascent_m,
            "sessions": w.sessions,
            "delta_pct": delta,
        })

        # prev_km = w.distance_km

    return {
        "schema_version": "v1",
        "season": season_block,
        "weeks": weeks_block,
        "summary_cards": summary_cards,
        "weekly_series": weekly_series,
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
