from __future__ import annotations

from pathlib import Path

import polars as pl

from src.models.season_config import SeasonConfig


class SeasonRepository:
    def __init__(self, path: str | None = 'data/config', season_code: str | None = None) -> None:
        self.config_path = Path(f"{path}/seasons.csv")
        self.season_code = season_code

    #-- - Lee todas las temporadas
    def load(self) -> list[SeasonConfig]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"No existe archivo de configuración: {self.config_path}")

        df = pl.read_csv(self.config_path).with_columns(
            pl.col("start_date").str.to_date()
        )

        seasons: list[SeasonConfig] = []

        for row in df.iter_rows(named=True):
            config = SeasonConfig(
                code=row["code"],
                season=int(row["season"]),
                start_date=row["start_date"],
                weeks=int(row["weeks"]),
                name=row.get("name", "") if isinstance(row, dict) else "",
            )

            if config.start_date is None:
                raise ValueError(f"start_date inválido en temporada {config.code}")

            seasons.append(config)

        # Ordenar por fecha de inicio (importante)
        seasons.sort(key=lambda s: s.start_date)

        return seasons

    #-- - Devuelve la tempodada solicitada
    def load_season(self) -> SeasonConfig:
        seasons = self.load()

        if self.season_code:
            for s in seasons:
                if s.code == self.season_code:
                    return s

        return SeasonConfig()
