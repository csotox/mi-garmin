#-- - file: src/extract.py

from typing import Any, Dict

from fitparse import FitFile

from src.analysis.activity_type import activity_type
from src.models.activity import ActivitySummary
from src.models.lap import LapSummary
from src.models.record import RecordPoint


def get_activity_summary(fitfile: FitFile, file_name: str) -> ActivitySummary:
    session = next(fitfile.get_messages("session"))

    data: Dict[str, Any] = {
        field.name: field.value
        for field in session  # type: ignore[reportGeneralTypeIssues]
    }

    # El .fit no siempre trae str para indicar el tipo de actividad
    # valido cuando viene int
    if isinstance( data["sport"], int ):
        data["sport"] = str(data["sport"])

    summary = ActivitySummary(
        activity_id = file_name,
        file_name=file_name,
        start_time=data["start_time"],
        sport=data["sport"],
        activity_type=activity_type(data["sport"]),

        total_distance=data["total_distance"],
        total_timer_time=data["total_timer_time"],

        avg_heart_rate=data.get("avg_heart_rate"),
        max_heart_rate=data.get("max_heart_rate"),

        total_ascent=data.get("total_ascent"),
        total_descent=data.get("total_descent"),
    )

    return summary

def get_activity_laps(fitfile: FitFile) -> list[LapSummary]:
    laps: list[LapSummary] = []

    for idx, lap in enumerate(fitfile.get_messages("lap")):
        data: Dict[str, Any] = {
            field.name: field.value
            for field in lap  # type: ignore[reportGeneralTypeIssues]
        }

        lap_summary = LapSummary(
            lap_index=idx,
            total_distance=data["total_distance"],
            total_timer_time=data["total_timer_time"],
            avg_heart_rate=data.get("avg_heart_rate"),
            max_heart_rate=data.get("max_heart_rate"),
            total_ascent=data.get("total_ascent"),
            total_descent=data.get("total_descent"),
        )

        laps.append(lap_summary)

    return laps

def get_activity_records(fitfile: FitFile, file_name: str) -> list[RecordPoint]:
    records: list[RecordPoint] = []

    for record in fitfile.get_messages("record"):
        data: Dict[str, Any] = {
            field.name: field.value
            for field in record  # type: ignore[reportGeneralTypeIssues]
        }

        if "timestamp" not in data:
            continue

        point = RecordPoint(
            activity_id=file_name,
            timestamp=data["timestamp"],
            heart_rate=data.get("heart_rate"),
            speed=data.get("speed"),
            altitude=data.get("altitude"),
        )

        records.append(point)

    return records
