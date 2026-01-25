import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

from src.dashboard.models import DashboardDataV1


class MatplotlibDashboard:

    def __init__(self, data: DashboardDataV1):
        self.data = data


    def build(self, mode: str = "window", output_path="data/outputs/dashboard_v1.png"):
        #                         Ancho  Alto
        fig = plt.figure(figsize=(   16,    8), constrained_layout=True)
        gs = GridSpec(3, 4, figure=fig, height_ratios=[0.6, 1.2, 2.2])

        self._draw_header(fig)
        self._draw_cards(fig, gs)
        self._draw_weekly_chart(fig, gs)

        if mode == 'imagen':
            plt.savefig(output_path, dpi=150)
            print(f"Dashboard generado: {output_path}")
        else:
            plt.show()

        plt.close()


    def _draw_header(self, fig):
        season = self.data.season

        title = f"Entrenamiento – {season.name}"
        subtitle = f"Semana {season.current_week} ({season.week_start} - {season.week_end})"

        fig.subplots_adjust(top=0.90, hspace=0.35)
        fig.suptitle(title, fontsize=18, fontweight="bold")
        fig.text(0.5, 0.915, subtitle, ha="center", fontsize=12)


    def draw_card(self, ax, title, value):
        rect = Rectangle((0, 0), 1, 1,
                        linewidth=1.2,
                        edgecolor="#444",
                        facecolor="#f9f9f9",
                        transform=ax.transAxes)

        ax.add_patch(rect)
        ax.text(0.06, 0.65, title, fontsize=10, color="#666", transform=ax.transAxes)
        ax.text(0.06, 0.30, value, fontsize=18, weight="bold", transform=ax.transAxes)


    def _draw_cards(self, fig, gs):
        cards = self.data.summary_cards

        values = [
            ("Km acumulados", f"{cards.total_km:.1f}"),
            ("Desnivel +", f"{cards.total_ascent_m} m"),
            ("Tiempo", f"{cards.total_time_min} min"),
            ("Sesiones", str(cards.total_sessions)),
        ]

        for i, (title, value) in enumerate(values):
            ax = fig.add_subplot(gs[1, i])
            ax.axis("off")
            self.draw_card(ax, title, value)


    def _draw_weekly_chart(self, fig, gs):
        ax = fig.add_subplot(gs[2, :])

        weeks = self.data.weekly_series
        microcycles = {m.week for m in self.data.microcycles}

        x = [w.week for w in weeks]
        km = [w.km for w in weeks]
        delta = [w.delta_pct for w in weeks]

        ax.bar(x, km, alpha=0.7, label="Km")

        # Línea de variación
        ax2 = ax.twinx()
        ax2.plot(x, delta, color="orange", marker="o", label="Δ %")

        # Microciclos
        for w in microcycles:
            ax.axvline(w, color="gray", linestyle="--", alpha=0.4)

        ax.set_title("Volumen semanal")
        ax.set_xlabel("Semana")
        ax.set_ylabel("Km")
        ax2.set_ylabel("Δ %")

        ax.grid(True, axis="y", alpha=0.3)

        ax.legend(loc="upper left")
        ax2.legend(loc="upper right")
