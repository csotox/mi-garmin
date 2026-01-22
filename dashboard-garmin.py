
TEMPORADA_CODE_DEFAULT = "T2026"


#-- - Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
#-- - consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
#-- - simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: object = '') -> None:
    print(msj)

def main():
    printx("-- - Generando Dashboard de entrenamiento de Garmin Connect -- -")

    #-- - 1.
    #-- - Leer archivos json

    printx("-- - Dashboard generado -- -")

if __name__ == "__main__":
    main()
