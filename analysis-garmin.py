import json
from pathlib import Path

from src.analysis.analysis import get_data_kpi_week_from_activity
from src.analysis.dashboard_v1_builder import build_dashboard_v1
from src.analysis.kpi_week_exporter import KPIWeekExporter
from src.analysis.kpi_week_repository import KPIWeekRepository
from src.analysis.repository import load_activity_summary
from src.analysis.season_repository import SeasonRepository

TEMPORADA_CODE_DEFAULT = "T2026"


#-- - Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
#-- - consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
#-- - simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: object = '') -> None:
    print(msj)

def main():
    printx("-- - Iniciando Análisis de entrenamiento de Garmin Connect -- -")

    #-- - 1.
    #-- - Configuración de temporada actual
    temporada = SeasonRepository(season_code=TEMPORADA_CODE_DEFAULT).load_season()
    printx(f"Temporada activa: {temporada.name} ({temporada.start_date} - {temporada.weeks} semanas)")

    #-- - 2.
    #-- - Carga de datos de actividades
    df_summary = load_activity_summary()
    printx(f"Total de actividades a procesar: {df_summary.height}")

    #-- - 3.
    #-- - Cálculo de KPIs/estadisticas
    kpis_week = get_data_kpi_week_from_activity(df_summary, temporada)
    # printx('-- - --')
    # printx(temporada)
    # printx(kpis_week)
    # printx('-- - --')

    #-- - 4.
    #-- - Persistencia del análisis
    #-- - Usando formato Parquet
    repo = KPIWeekRepository()
    repo.save(kpis_week)

    #-- - 5.
    #-- - Exportación a JSON (De aquí se genera el dashboard)
    exporter = KPIWeekExporter(season=temporada)
    exporter.export_all()

    data_for_json = build_dashboard_v1(temporada, kpis_week)

    output_path = Path("data/outputs/dashboard_v1.json")
    output_path.write_text(
        json.dumps(data_for_json, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    printx("-- - Análisis finalizado -- -")

if __name__ == "__main__":
    main()
