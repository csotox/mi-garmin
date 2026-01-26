#-- - file: src/transform.py

import polars as pl

from src.models.activity import ActivitySummary
from src.models.lap import LapSummary
from src.models.record import RecordPoint


def activity_summary_to_df(summary: list[ActivitySummary]) -> pl.DataFrame:
    return pl.DataFrame([s.model_dump() for s in summary])

def laps_to_df(laps: list[LapSummary]) -> pl.DataFrame:
    return pl.DataFrame([lap.model_dump() for lap in laps])

def records_to_df(records: list[RecordPoint]) -> pl.DataFrame:
    return pl.DataFrame([record.model_dump() for record in records])
