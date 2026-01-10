#-- - file: etl-garmin.py

from pathlib import Path

import polars as pl
from fitparse import FitFile

from src.etl.extract import get_activity_laps, get_activity_records, get_activity_summary
from src.etl.load import write_parquet
from src.etl.transform import activity_summary_to_df, laps_to_df, records_to_df
from src.models.activity import ActivitySummary

PATH_DATA_RAW = 'data/raw_data'
PATH_DATA_PARQUET = 'data/parquet'

#-- - Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
#-- - consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
#-- - simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: object = '') -> None:
    print(msj)

#-- - Lectura de datos desde la carpeta data/raw_data/...
#-- -
#-- - Como Garmin Connect no proporciona una API pública, o tiene requisitos para acceder a la misma,
#-- - La parte de obtener los datos se realizara de forma manual descargando los archivos desde la
#-- - web y copiando estos archivos en la carpeta data/raw_data/
#-- - [TODO] Solo si es necesario aplicar scraping, pero no creo que sea el caso en este momento.
#-- -
#-- - Considerar que revisando la página de Garmin Connect descargar los csv de las actividades
#-- - no contienen suficiente información para el análisis que deseo realizar. Por tanto,
#-- - Intentaremos trabajar con los archivos .fit Mucha suerte y animo :)
def read_raw_fit_activities() -> tuple[list[ActivitySummary], list, list]:
    activities: list[ActivitySummary] = []
    all_laps = []
    all_records = []

    base_path = Path(f"{PATH_DATA_RAW}/fit_activities")
    fit_files = list(base_path.glob("*.fit"))

    fit_count = len(fit_files)
    printx(f"Procesando {fit_count} archivos")

    for item_file in fit_files:
        data = FitFile( str(item_file) )

        summary = get_activity_summary(data)
        activities.append(summary)

        laps = get_activity_laps(data)
        all_laps.extend(laps)

        records = get_activity_records(data)
        all_records.extend(records)

    return activities, all_laps, all_records

def main():
    printx("-- - Iniciando Automatización de Garmin Connect -- -")

    #-- - Leer archivos .fit para data de actividad deportiva
    activities, laps, records = read_raw_fit_activities()

    #-- - Transformar data a DataFrames
    df_activity = activity_summary_to_df(activities[0])         # Vamos poco a poco
    df_laps = laps_to_df(laps)
    df_records = records_to_df(records)

    #-- - Persistencia de datos
    write_parquet(df_activity, f"{PATH_DATA_PARQUET}/activity_summary.parquet")
    write_parquet(df_laps, f"{PATH_DATA_PARQUET}/laps.parquet")
    write_parquet(df_records, f"{PATH_DATA_PARQUET}/records.parquet")

    #-- - Validación de todo ok
    df_check = pl.read_parquet(f"{PATH_DATA_PARQUET}/activity_summary.parquet")
    printx(df_check)


    printx("-- - Automatización finalizada -- -")

if __name__ == "__main__":
    main()
