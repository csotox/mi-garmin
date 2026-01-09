from pathlib import Path

from fitparse import FitFile

PATH_DATA_RAW = 'data/raw_data'

# Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
# consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
# simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: str = '') -> None:
    print(msj)

def read_raw_fit_activities():
    base_path = Path(f"{PATH_DATA_RAW}/fit_activities")
    fit_files = list(base_path.glob("*.fit"))

    fit_count = len(fit_files)
    printx(f"Procesando {fit_count} archivos")

    for item_file in fit_files:
        data = FitFile( str(item_file) )

        message_types = set()
        for msg in data.get_messages():
            message_types.add(msg.name)

        printx(f"Tipos de mensajes encontrados: {sorted(message_types)}")

        # Ver información en session
        for session in data.get_messages("session"):
            printx("Resumen de sesión:")
            for field in session:
                printx(f"  {field.name}: {field.value}")

            break

    return []

def main():
    printx("-- - Iniciando Automatización de Garmin Connect -- -")

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
    activities = read_raw_fit_activities()

    printx("-- - Automatización finalizada -- -")

if __name__ == "__main__":
    main()
#