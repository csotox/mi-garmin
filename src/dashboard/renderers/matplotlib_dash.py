import math

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

from src.dashboard.renderers.base import DashboardRenderer


class MatplotlibRenderer(DashboardRenderer):


    def __init__(self, mode="window", output_path="data/outputs/dashboard_v1.png"):
        self.mode = mode
        self.output_path = output_path

        self.fig = plt.figure(figsize=(16, 8), constrained_layout=True)
        self.gs = GridSpec(3, 4, figure=self.fig, height_ratios=[0.6, 1.2, 2.2])


    def render_header(self, data):
        season = data.season
        title = f"Entrenamiento – {season.name}"
        subtitle = f"Semana {season.current_week} ({season.week_start} - {season.week_end})"

        self.fig.suptitle(title, fontsize=18, fontweight="bold")
        self.fig.text(0.5, 0.92, subtitle, ha="center", fontsize=12)


    def render_cards(self, data):
        cards = data.summary_cards

        values = [
            ("Sesiones", str(cards.total_sessions)),
            ("Km acumulados", f"{cards.total_km:.1f}"),
            ("Desnivel +", f"{cards.total_ascent_m} m"),
            ("Tiempo", f"{cards.total_time_min} min"),
        ]

        for i, (title, value) in enumerate(values):
            ax = self.fig.add_subplot(self.gs[1, i])
            ax.axis("off")

            rect = Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                             linewidth=1.2, edgecolor="#444", facecolor="#f9f9f9")
            ax.add_patch(rect)

            ax.text(0.06, 0.65, title, fontsize=10, color="#666", transform=ax.transAxes)
            ax.text(0.06, 0.30, value, fontsize=18, weight="bold", transform=ax.transAxes)

    def render_weeks_table(self, data):
        ...

    def render_weekly_chart(self, data):
        ax = self.fig.add_subplot(self.gs[2, :])

        weeks = data.weekly_series
        microcycles = {m.week for m in data.microcycles}

        x = [w.week for w in weeks]
        km = [w.km for w in weeks]
        delta = [
            w.delta_pct if w.delta_pct is not None else math.nan
            for w in weeks
        ]

        ax.bar(x, km, alpha=0.7, label="Km")

        ax2 = ax.twinx()
        ax2.plot(x, delta, color="orange", marker="o", label="Δ %")

        for w in microcycles:
            ax.axvline(w, color="gray", linestyle="--", alpha=0.4)

        ax.set_title("Volumen semanal")
        ax.set_xlabel("Semana")
        ax.set_ylabel("Km")
        ax2.set_ylabel("Δ %")

        ax.grid(True, axis="y", alpha=0.3)
        ax.legend(loc="upper left")
        ax2.legend(loc="upper right")


    def finalize(self):
        if self.mode == "imagen":
            plt.savefig(self.output_path, dpi=150)
            print(f"Dashboard generado: {self.output_path}")
        else:
            plt.show()

        plt.close()
