from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.activity import ActivitySummary


def test_activity_summary_valid():
    summary = ActivitySummary(
        start_time=datetime.now(),      # Fecha/hora inicio de la actividad
        sport="running",                #
        total_distance=5000.0,          # 5 kilometros
        total_timer_time=1800.0,        # 30 minutos
        avg_heart_rate=140,             # Pulso promedio
        max_heart_rate=160,             # Pulso maximo durante la actividad
        total_ascent=120,               # Mts desnivel positivo
        total_descent=110,              # Mts desnivel negativo
    )

    assert summary.total_distance > 0
    assert summary.sport == "running"


def test_activity_summary_missing_required_field():
    invalid_data = {
        "start_time": datetime.now(),
        "sport": "running",
        "total_timer_time": 1800.0,
    }

    with pytest.raises(ValidationError):
        ActivitySummary(**invalid_data)
