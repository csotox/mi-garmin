
# Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
# consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
# simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: str = '') -> None:
    print(msj)

def read_raw_fit_activities():
    ...


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
