from fitparse import FitFile

from src.extract import get_activity_summary
from src.models.activity import ActivitySummary


def test_get_activity_summary_from_fit(tmp_path):
    fit_path = "tests/fixtures/Activity.fit"

    fitfile = FitFile(fit_path)
    summary = get_activity_summary(fitfile)

    assert isinstance(summary, ActivitySummary)
    assert summary.total_distance > 0
    assert summary.sport == "running"
