from fitparse import FitFile

from src.extract import get_activity_laps
from src.models.lap import LapSummary


def test_extract_laps_from_fit():
    fit_path = "tests/fixtures/Activity.fit"
    fitfile = FitFile(fit_path)
    laps = get_activity_laps(fitfile)

    assert len(laps) > 0
    assert isinstance(laps[0], LapSummary)
    assert laps[0].total_distance > 0
