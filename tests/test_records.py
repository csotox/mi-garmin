from fitparse import FitFile

from src.etl.extract import get_activity_records
from src.models.record import RecordPoint


def test_extract_records():
    fit_path = "tests/fixtures/Activity.fit"
    fitfile = FitFile(fit_path)

    records = get_activity_records(fitfile)

    assert len(records) > 0
    assert isinstance(records[0], RecordPoint)
    assert records[0].timestamp is not None
