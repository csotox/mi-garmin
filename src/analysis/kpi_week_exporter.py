from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from src.analysis.kpi_week_repository import KPIWeekRepository


class KPIWeekExporter:
    def __init__(
        self,
        parquet_path: str = "data/parquet",
        output_path: str = "data/outputs",
    ) -> None:
        self.repo = KPIWeekRepository(base_path=parquet_path)

        self.output_dir = Path(output_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = self.output_dir / "kpi_week.json"

    def export_all(self) -> None:
        df = self.repo.load()
        self._export_df(df)

    def export_season(self, season_code: str) -> None:
        df = self.repo.load_by_season(season_code)
        self._export_df(df, season_code)

    def _export_df(self, df: pl.DataFrame, season_code: str | None = None) -> None:
        payload = {
            "season": season_code,
            "generated_at": datetime.now(UTC).isoformat(),
            "weeks": df.to_dicts() if not df.is_empty() else [],
        }

        self.output_file.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
