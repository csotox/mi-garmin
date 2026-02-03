from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import polars as pl

from src.analysis.kpi_week_repository import KPIWeekRepository
from src.models.season_config import SeasonConfig


class KPIWeekExporter:
    def __init__(
        self,
        season: SeasonConfig,
        parquet_path: str = "data/parquet",
        output_path: str = "data/outputs",
    ) -> None:
        self.repo = KPIWeekRepository(base_path=parquet_path)

        self.output_dir = Path(output_path)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = self.output_dir / "kpi_week.json"

        self.season = season

    def export_all(self) -> None:
        df = self.repo.load()
        self._export_df(df)

    def export_season(self) -> None:
        df = self.repo.load_by_season(self.season.code)
        self._export_df(df)

    def _export_df(self, df: pl.DataFrame) -> None:
        payload = {
            "schema_version": "v1",
            "season": {
                "code": self.season.code,
                "season": self.season.season,
                "name": self.season.name,
                "start_date": self.season.start_date.isoformat(),
                "weeks": self.season.weeks,
            } if self.season else None,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "weeks": df.to_dicts() if not df.is_empty() else [],
        }

        self.output_file.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
