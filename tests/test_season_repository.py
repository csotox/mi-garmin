from datetime import date
from pathlib import Path

from src.analysis.season_repository import SeasonRepository
from src.models.season_config import SeasonConfig


def get_fixture_path(filename: str) -> Path:
    return Path(__file__).parent / "fixtures" / filename

def test_load_seasons_ok(tmp_path: Path):
    csv_path = get_fixture_path("seasons.csv")

    repo = SeasonRepository()
    repo.config_path = csv_path

    seasons = repo.load()

    assert len(seasons) == 1
    assert isinstance(seasons[0], SeasonConfig)
    assert seasons[0].code == "T2026"
    assert seasons[0].season == 26
    assert seasons[0].start_date == date(2025, 10, 13)
    assert seasons[0].weeks == 40


def test_load_season_by_code(tmp_path: Path):
    csv_path = get_fixture_path("seasons.csv")

    repo = SeasonRepository(season_code="T2026")
    repo.config_path = csv_path

    season = repo.load_season()

    assert season.code == "T2026"
    assert season.season == 26


def test_load_season_not_found(tmp_path: Path):
    csv_path = get_fixture_path("seasons.csv")

    repo = SeasonRepository(season_code="T9999")
    repo.config_path = csv_path

    season = repo.load_season()

    assert season.code == ""
    assert season.season == 0
    assert season.start_date == date(2026, 1, 1)
    assert season.weeks == 0
