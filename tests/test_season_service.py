from datetime import date

from src.analysis.season_service import build_season_code, calculate_season_week
from src.models.season_config import SeasonConfig


#-- - No voy a usar el fixture. Quiero que este código se mantenga constante
#-- - probablemente más adelante el fixture seasons.csv va a cambiar y no
#-- - quiero que afecte estas pruebas. Así que dejo el config fijo.
def get_season() -> SeasonConfig:
    return SeasonConfig(
        code="T2026",
        season=26,
        start_date=date(2025, 10, 13),
        weeks=40,
        name="Temporada 2026",
    )


def test_calculate_season_week_basic():
    season = get_season()

    activity_date = date(2026, 1, 8)  # semana 13

    week = calculate_season_week(activity_date, season)

    assert week == 13


#-- - En caso que la fecha de la actividad esta fuera de la temporada.
#-- - En esta caso la fecha puede pertenecer a la temporada anterior.
def test_calculate_season_week_before_season():
    season = get_season()

    activity_date = date(2025, 10, 1)

    week = calculate_season_week(activity_date, season)

    assert week == 0


#-- - En este caso la fecha de la actividad es posterior a la fecha final de la temporada actual.
#-- - Regreso -1 para que sea visualmente más claro, que ocurre un error con las semanas.
#-- - Las semanas de una temporada puede variar, para una temporada pueden ser 40
#-- - y la temporada siguiente pueden ser 45 semanas.
def test_calculate_season_week_after_season_end():
    season = get_season()

    activity_date = date(2026, 12, 31)

    week = calculate_season_week(activity_date, season)

    assert week == -1


def test_build_season_code():
    season = get_season()

    code = build_season_code(season, 13)

    assert code == "T2026.13"
