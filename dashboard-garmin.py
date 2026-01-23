from src.dashboard.builder import DashboardBuilder
from src.dashboard.loader import DashboardLoader

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
    #-- - OJO estoy usando dashboard_v1.json es un json fake para pruebas
    #-- -     para tener los datos necesarios para generar el dashboard
    data = DashboardLoader("data/outputs/dashboard_v1.json").load().parse()

    #-- - 2.
    #-- - Generación de dashboard
    DashboardBuilder(data).build_console()

    printx("-- - Dashboard generado -- -")

if __name__ == "__main__":
    main()
