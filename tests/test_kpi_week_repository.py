from datetime import date
from pathlib import Path

import polars as pl

from src.analysis.kpi_week_repository import KPIWeekRepository
from src.models.data_kpi_week import DataKPIWeek


def test_save_kpi_week(tmp_path: Path):
    repo = KPIWeekRepository(base_path=str(tmp_path))

    kpi = DataKPIWeek(
        season=26,
        season_week=13,
        season_code="T26.13",
        week_start=date(2026, 1, 8),
        week_end=date(2026, 1, 9),
        sessions=2,
        distance_km=12.0,
        time_min=70.0,
        ascent_m=300,
        descent_m=270,
        avg_heart_rate=145.0,
        max_heart_rate=170,
    )

    repo.save([kpi])

    parquet_file = tmp_path / "kpi_week.parquet"
    assert parquet_file.exists()

    df = pl.read_parquet(parquet_file)

    assert df.height == 1
    assert df["season"][0] == 26
    assert df["season_week"][0] == 13
    assert df["distance_km"][0] == 12.0

def test_load_empty(tmp_path):
    repo = KPIWeekRepository(base_path=str(tmp_path))
    df = repo.load()
    assert df.is_empty()

def test_overwrite_season(tmp_path):
    repo = KPIWeekRepository(base_path=str(tmp_path))

    kpi1 = DataKPIWeek(season=26, season_week=1, season_code="T26.01", week_start=date(2025, 10, 13), week_end=date(2025, 10, 19))
    kpi2 = DataKPIWeek(season=26, season_week=2, season_code="T26.02", week_start=date(2025, 10, 20), week_end=date(2025, 10, 26))

    repo.save([kpi1, kpi2])

    new_kpi = DataKPIWeek(season=26, season_week=1, season_code="T26.01", week_start=date(2025, 10, 13), week_end=date(2025, 10, 19), sessions=5)

    repo.overwrite_season("T26.01", [new_kpi])

    df = repo.load()

    assert df.height == 2
    assert df.filter(pl.col("season_week") == 1)["sessions"][0] == 5
