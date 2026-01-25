from abc import ABC, abstractmethod

from src.dashboard.models import DashboardDataV1


class DashboardRenderer(ABC):

    @abstractmethod
    def render_header(self, data: DashboardDataV1): ...

    @abstractmethod
    def render_cards(self, data: DashboardDataV1): ...

    @abstractmethod
    def render_weekly_chart(self, data: DashboardDataV1): ...

    @abstractmethod
    def render_weeks_table(self, data: DashboardDataV1): ...

    @abstractmethod
    def finalize(self): ...
