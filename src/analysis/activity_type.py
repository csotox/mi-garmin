from __future__ import annotations


def activity_type(sport: str | None) -> str:
    if not sport:
        return "other"

    value = sport.lower()

    if value in {"running", "trail_running"}:
        return "run"

    if value in {"walking", "hiking"}:
        return "walk"

    if value in {"hiit", "cardio"}:
        return "gym"

    return "other"
