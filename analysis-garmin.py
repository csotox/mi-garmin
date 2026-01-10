from src.analysis.analysis import get_data_kpi_week_from_activity
from src.analysis.repository import load_activity_summary


#-- - Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
#-- - consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
#-- - simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: object = '') -> None:
    print(msj)

def main():
    printx("-- - Iniciando Análisis de entrenamiento de Garmin Connect -- -")

    df_summary = load_activity_summary()
    kpis_week = get_data_kpi_week_from_activity(df_summary)

    print(f"Total actividades: {df_summary.height}")
    print(kpis_week)

    printx("-- - Análisis finalizado -- -")

if __name__ == "__main__":
    main()
