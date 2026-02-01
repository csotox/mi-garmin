# Automatización de análisis de registro en Garmin

## Descripción general

Este proyecto implementa un pipeline ETL para procesar actividades deportivas exportadas desde Garmin Connect en formato .fit, almacenarlas en formato analítico (Parquet) y generar salidas estructuradas (JSON) para análisis y visualización.

## Proceso ETL

- Descarga manual de archivos desde Garmin
- Extracción
  - Lee archivos .fit descargados
- Transformación
  - Convierte las listas/dict en df
- Persistencia
  - Se crean archivos Parquet con la información de:
    - Actividades (session)
    - Vueltas (laps)
    - Registros (records)

### Proceso de análisis

- Lectura de archivos Parquet.
- Cálculo de métricas deportivas.
- Generación de archivos JSON para consumo por:
  - Preparador físico
  - Entrenador de trail
  - Vista de entrenamiento

## Estructura inicial del proyecto

~~~ md
mi-garmin/
├─ data/
│  ├─ raw_data/              # Data original
│  │  └─ fit_activities/     # Archivos .fit descargados desde Garmin Connect
│  ├─ parquet/               # Capa de persistencia
│  └─ outputs/               # JSON para análisis
├─ src/
│  ├─ analysis/                  # Análisis de datos y generación de kpis
│  │  ├─ activity_type.py        # Homologación de tipos de entrenamiento
│  │  ├─ analysis.py             # Calcula kpis y análisis semanal
│  │  ├─ kpi_week_exporter.py    # Genera json para visualización/Dashboard
│  │  ├─ kpi_week_repository.py  # 
│  │  ├─ repository.py           # Lee los archivos parquet (raw)
│  │  ├─ season_repository.py    # Calculos de temporada
│  │  └─ season_service.py       # Helper/utils para calculos de config de la temporada
│  ├─ dashboard/                 # Generación del Dashboard
│  │  ├─ renders/                # Templates para generar los dashboard
│  │  └─ files.varios            # 
│  ├─ etl/                # Código ETL
│  │  ├─ extract.py       # Lectura de carpeta raw_data
│  │  ├─ transform.py     # Procesamiento y normalización de los datos
│  │  └─ load.py          # Actualización de archivos Parquet
│  └─ models/             # Models de pydantic
│  └─ utils/              # Utilidades / Helpres
│  │  └─ printx.py        # Salida por consola, progress bar
│  ├─ export.py           # parquet -> JSON (Generar json para análisis)
│  └─ reports.py          # Generación de tablero analítico
├─ tests/
│  ├─ test_extract.py
│  ├─ test_transform.py
│  ├─ test_load.py
│  ├─ test_export.py
│  └─ test_reports.py
├─ analysis_garmin.py     # pipelines para calculo del análisis
└─ etl-garmin.py          # Lanzados de la automatización
~~~

## Stack

- Docker
- Python 3.13
- Polars
- Matplotlib + Seaborn
- logging
- pydantic
- fitparse
- pytest

## Decisiones de diseño

- La obtención de los archivos .fit desde Garmin Connect se realiza de forma manual. No se implementó scraping para evitar posibles problemas legales o de mantenimiento. No aplico consumo de la APIs de Garmin porque creo que no cumplo las condiciones para tener acceso. Esto es un punto que se puede verificar más adelante.
- El pipeline esta pensado para correr en local con Docker.
- La persistencia de datos se basa en archivos Parquet, en lugar de una base de datos (por ejemplo SQLite), por mantener simplicidad.
- El proyecto está diseñado bajo el principio de separación de responsabilidades:
  - El proceso ETL solo construye datos confiables.
  - La capa de análisis genera conocimiento.
  - La visualización es un componente independiente.

## Lo que depara el futuro

- Análisis temporal avanzado.
- Análisis de ruta técnica a partir de puntos GPS

