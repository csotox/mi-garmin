from pathlib import Path

import polars as pl


def write_parquet(df: pl.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path)
