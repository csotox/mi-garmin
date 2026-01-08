# Automatización de análisis de registro en Garmin

## Proceso ETL

- Descarga manual de archivos desde Garmin
  - ...
- Transformación y normalización de los datos obtenidos
  - Gestión de duplicados.
  - ...
- Actualización de archivos Parquet (Capa de persistencia normalizada)
- Generación de archivos JSON (Usados para análisis de datos)

## Estructura inicial del proyecto

~~~ md
mi-garmin/
├─ data/
│  ├─ raw_data/    # Data original
│  ├─ parquet/     # Capa de persistencia
│  └─ outputs/     # JSON para análisis
├─ src/
│  ├─ extract.py       # Lectura de carpeta raw_data
│  ├─ transform.py     # Procesamiento y normalización de los datos
│  ├─ load.py          # Actualización de archivos Parquet
│  ├─ export.py        # parquet -> JSON (Generar json para análisis)
│  └─ reports.py       # Generación de tablero analitico
├─ tests/
│  ├─ test_extract.py
│  ├─ test_transform.py
│  ├─ test_load.py
│  ├─ test_export.py
│  └─ test_reports.py
└─ etl-garmin.py       # Lanzados de la automatización
~~~

## Stack

- Python 3.13
- Polars
- Matplotlib + Seaborn
- logging
