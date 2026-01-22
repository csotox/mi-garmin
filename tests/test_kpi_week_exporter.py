import json
from datetime import date
from pathlib import Path

from src.analysis.kpi_week_exporter import KPIWeekExporter
from src.analysis.kpi_week_repository import KPIWeekRepository
from src.models.data_kpi_week import DataKPIWeek
from src.models.season_config import SeasonConfig


def test_export_all(tmp_path: Path):
    parquet_dir = tmp_path / "parquet"
    output_dir = tmp_path / "outputs"

    repo = KPIWeekRepository(base_path=str(parquet_dir))

    temporada = SeasonConfig(
        code="T2026",
        season=26,
        start_date=date(2025,10,13),
        weeks=40,
        name="Temporada 2026"
    )


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

    exporter = KPIWeekExporter(
        season=temporada,
        parquet_path=str(parquet_dir),
        output_path=str(output_dir),
    )

    exporter.export_all()

    output_file = output_dir / "kpi_week.json"
    assert output_file.exists()

    data = json.loads(output_file.read_text())

    assert "generated_at" in data
    assert len(data["weeks"]) == 1
    assert data["weeks"][0]["season_week"] == 13
