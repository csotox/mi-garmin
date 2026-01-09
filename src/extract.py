from fitparse import FitFile

from src.models.activity import ActivitySummary


def get_activity_summary(fitfile: FitFile) -> ActivitySummary:
    session = next(fitfile.get_messages("session"))

    data = {field.name: field.value for field in session}

    summary = ActivitySummary(
        start_time=data["start_time"],
        sport=data["sport"],

        total_distance=data["total_distance"],
        total_timer_time=data["total_timer_time"],

        avg_heart_rate=data.get("avg_heart_rate"),
        max_heart_rate=data.get("max_heart_rate"),

        total_ascent=data.get("total_ascent"),
        total_descent=data.get("total_descent"),
    )

    return summary
