from src.dashboard.models import DashboardDataV1
from src.dashboard.render import (
    render_cards,
    render_header,
    render_weekly_chart,
    render_weeks_table,
)


class DashboardBuilder:
    def __init__(self, data: DashboardDataV1) -> None:
        self.data = data

    def build_console(self):
        render_header(self.data.season)
        render_cards(self.data.summary_cards)
        render_weeks_table(self.data.weekly_series)
        render_weekly_chart(self.data.weekly_series, self.data.microcycles)

        return self
