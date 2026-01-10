from __future__ import annotations

from pathlib import Path

import polars as pl

PATH_PARQUET_DIR = Path("data/parquet")


def load_activity_summary() -> pl.DataFrame:
    return pl.read_parquet(f"{PATH_PARQUET_DIR}/activity_summary.parquet")

def load_laps() -> pl.DataFrame:
    return pl.read_parquet(f"{PATH_PARQUET_DIR}/laps.parquet")

def load_records() -> pl.DataFrame:
    return pl.read_parquet(f"{PATH_PARQUET_DIR}/records.parquet")
