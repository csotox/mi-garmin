from src.analysis.analysis import get_data_kpi_week_from_activity
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

    #-- - 4.
    #-- - Persistencia del análisis
    #-- - Usando formato Parquet
    repo = KPIWeekRepository()
    repo.save(kpis_week)

    #-- - 5.
    #-- - Exportación a JSON (De aquí se genera el dashboard)
    exporter = KPIWeekExporter()
    exporter.export_all()

    printx("-- - Análisis finalizado -- -")

if __name__ == "__main__":
    main()
