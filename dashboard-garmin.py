import sys

from src.dashboard.builder import DashboardBuilder
from src.dashboard.loader import DashboardLoader
from src.dashboard.renderers.consola_dash import ConsolaRenderer
from src.dashboard.renderers.matplotlib_dash import MatplotlibRenderer

TEMPORADA_CODE_DEFAULT = "T2026"


#-- - Probablemente esta función sea temporal, quiero ver como se comporta cuando muestre mensajes en
#-- - consola. Me gustaria agregar color y probablemente barras de progreso. Por ahora lo mantenemos
#-- - simple. Si no se logra el objetivo, siempre se puede usar logging.
def printx(msj: object = '') -> None:
    print(msj)

def main():
    printx("-- - Generando Dashboard de entrenamiento de Garmin Connect -- -")

    #-- - Argumento vía consola
    modo = sys.argv[1] if len(sys.argv) > 1 else "matplotlib"

    #-- - 1.
    #-- - Leer archivos json
    #-- - OJO estoy usando dashboard_v1.json es un json fake para pruebas
    #-- -     para tener los datos necesarios para generar el dashboard
    data = DashboardLoader("data/outputs/dashboard_v1.json").load().parse()

    #-- - 2.
    #-- - Generación de dashboard
    if modo == "consola":
        renderer = ConsolaRenderer()
    else:
        renderer = MatplotlibRenderer(mode="window")

    DashboardBuilder(data, renderer).build()

    printx("-- - Dashboard generado -- -")

if __name__ == "__main__":
    main()
