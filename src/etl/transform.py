#-- - file: src/etl/transform.py

import polars as pl

from src.models.activity import ActivitySummary
from src.models.lap import LapSummary
from src.models.record import RecordPoint


def activity_summary_to_df(activities: list[ActivitySummary]) -> pl.DataFrame:
    return (
        pl.DataFrame([a.model_dump() for a in activities])
        .sort("start_time")
        .with_row_index("activity_id")
    )

def laps_to_df(laps: list[LapSummary]) -> pl.DataFrame:
    return pl.DataFrame([lap.model_dump() for lap in laps])

def records_to_df(records: list[RecordPoint]) -> pl.DataFrame:
    return pl.DataFrame([record.model_dump() for record in records])
