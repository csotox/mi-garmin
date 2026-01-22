from __future__ import annotations

from pathlib import Path
from typing import Iterable

import polars as pl

from src.models.data_kpi_week import DataKPIWeek


class KPIWeekRepository:
    def __init__(self, base_path: str = "data/parquet") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.file_path = self.base_path / "kpi_week.parquet"

    def save(self, kpis: Iterable[DataKPIWeek]) -> None:
        rows = [kpi.model_dump() for kpi in kpis]

        if not rows:
            return

        df = pl.DataFrame(rows)
        final_df = df

        if self.file_path.exists():
            existing = pl.read_parquet(self.file_path)

            if not existing.is_empty():
                new_keys = df.select(["season", "season_week"])

                existing = existing.join(
                    new_keys,
                    on=["season", "season_week"],
                    how="anti",
                )

                final_df = pl.concat([existing, df], how="vertical")

        final_df.write_parquet(self.file_path)


    def load(self) -> pl.DataFrame:
        if not self.file_path.exists():
            return pl.DataFrame([])

        return pl.read_parquet(self.file_path)

    def load_by_season(self, season_code: str) -> pl.DataFrame:
        df = self.load()
        if df.is_empty():
            return df

        return df.filter(pl.col("season_code") == season_code)

    def overwrite_season(self, season_code: str, kpis: Iterable[DataKPIWeek]) -> None:
        new_rows = [kpi.model_dump() for kpi in kpis]
        new_df = pl.DataFrame(new_rows) if new_rows else pl.DataFrame([])

        if self.file_path.exists():
            existing = pl.read_parquet(self.file_path)

            filtered = existing.filter(pl.col("season_code") != season_code)
            final_df = pl.concat([filtered, new_df], how="vertical")
        else:
            final_df = new_df

        final_df.write_parquet(self.file_path)
