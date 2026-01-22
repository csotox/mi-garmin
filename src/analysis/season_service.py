from __future__ import annotations

from datetime import date, timedelta

from src.models.season_config import SeasonConfig


#-- - Calcula la semana de la temporada a partir de la fecha de actividad.
#-- - Calculo:
#-- -  Se calcula la diferencia en días entre la fecha de la actividad y la fecha de inicio de la temporada.
#-- -  Con esto obtenemos los días transcurridos desde el inicio de la temporada. Luego calculamos la
#-- -  división por 7, para obtener el número de semanas.
def calculate_season_week(activity_date: date, season: SeasonConfig) -> int:
    diff_date = (activity_date - season.start_date).days

    if diff_date < 0:
        return 0  # actividad fuera de temporada (antes)

    weeks = (diff_date // 7) + 1

    if weeks > season.weeks:
        return -1  # La actividad esta fuera de la tempodada, entonces aquí hay un error en la configuración

    return weeks

#-- - Código de la temporada semana
#-- - Formato: TYY.SS
def build_season_code(season: SeasonConfig, season_week: int) -> str:
    return f"{season.code}.{season_week:02d}"

#-- - Devuelve el rango de inicio y fin de la semana
#-- - Por ahora se asume que la semana inicia el día lunes y termina el domingo
def get_season_week_range(season: SeasonConfig, week: int) -> tuple[date, date]:
    start = season.start_date + timedelta(days=(week - 1) * 7)
    end = start + timedelta(days=6)
    return start, end
