#-- - file: etl-garmin.py

from pathlib import Path

from fitparse import FitFile

from src.extract import get_activity_laps, get_activity_records, get_activity_summary
from src.models.activity import ActivitySummary

PATH_DATA_RAW = 'data/raw_data'

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
def read_raw_fit_activities() -> list[ActivitySummary]:
    activities: list[ActivitySummary] = []

    base_path = Path(f"{PATH_DATA_RAW}/fit_activities")
    fit_files = list(base_path.glob("*.fit"))

    fit_count = len(fit_files)
    printx(f"Procesando {fit_count} archivos")

    for item_file in fit_files:
        data = FitFile( str(item_file) )

        summary = get_activity_summary(data)
        activities.append(summary)

        laps = get_activity_laps(data)
        printx(f"Laps extraídos: {len(laps)}")
        for lap in laps:
            printx(lap.model_dump())

        records = get_activity_records(data)
        printx(f"Records extraídos: {len(records)}")
        printx(records[0].model_dump())

    return activities

def main():
    printx("-- - Iniciando Automatización de Garmin Connect -- -")

    activities = read_raw_fit_activities()

    printx(f"Se procesaron {len(activities)} actividades.")
    for item in activities:
        printx(item.model_dump())

    printx("-- - Automatización finalizada -- -")

if __name__ == "__main__":
    main()
