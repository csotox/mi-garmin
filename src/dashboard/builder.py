from src.dashboard.models import DashboardDataV1
from src.dashboard.renderers.base import DashboardRenderer


class DashboardBuilder:

    def __init__(self, data: DashboardDataV1, renderer: DashboardRenderer):
        self.data = data
        self.renderer = renderer

    def build(self):
        self.renderer.render_header(self.data)
        self.renderer.render_cards(self.data)
        self.renderer.render_weeks_table(self.data)
        self.renderer.render_weekly_chart(self.data)
        self.renderer.finalize()
        return self
