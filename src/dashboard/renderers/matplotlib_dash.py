import math
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch, Rectangle

from src.dashboard.renderers.base import DashboardRenderer

COLOR_FONDO    = "#e6e6e6"
COLOR_ENCABEZA = "#e8f4fb"
COLOR_W_HECHA  = "#c68642"
COLOR_W_CERRO  = "#8e5ea2"
COLOR_W_FUTURA = "#E8E5E5"
COLOR_F_TRAIL  = "#C2BFBF"      # Semana futura en cerro / trail
COLOR_W_NONE   = "#dddddd"
COLOR_DESAFIO  = "#c0392b"
COLOR_W_MIN    = "#34495e"
COLOR_W_INC    = "#f8c471"
DIAS_ES = ["L", "M", "X", "J", "V", "S", "D"]

class MatplotlibRenderer(DashboardRenderer):

    def __init__(self, mode="window", output_path="data/outputs/dashboard_v1.png"):
        self.mode = mode
        self.output_path = output_path

        self.fig = plt.figure(figsize=(16, 9), constrained_layout=True)
        self.gs = GridSpec(6, 4, figure=self.fig, height_ratios=[0.6, 1.2, 2.2, 1.6, 1.8, 1.2])


    def render_header(self, data):
        season = data.season
        title = f"Entrenamiento – {season.name}"
        subtitle = f"Semana {season.current_week} ({season.week_start} - {season.week_end})"

        self.fig.suptitle(title, fontsize=18, fontweight="bold")
        self.fig.text(0.5, 0.92, subtitle, ha="center", fontsize=12)


    def render_cards(self, data):
        cards = data.summary_cards

        # Calculo la media semanal
        weeks = data.weekly_series

        prom_km = sum(w.km for w in weeks) / len(weeks)
        prom_des = sum(w.ascent_m for w in weeks) / len(weeks)
        prom_time_min = minutes_to_hhmm(round(cards.total_time_min / len(weeks)))

        values = [
            ("Sesiones", str(cards.total_sessions), ""),
            ("Km acumulados", f"{cards.total_km:.0f} km", f"({prom_km:.1f} km/semana)"),
            ("Desnivel +", f"{cards.total_ascent_m:,} m".replace(",", "."), f"({prom_des:.1f} m/semana)"),
            ("Tiempo", f"{minutes_to_hhmm(int(cards.total_time_min))}", f"({prom_time_min} min/semana)"),
        ]

        for i, (title, value, sub) in enumerate(values):
            ax = self.fig.add_subplot(self.gs[1, i])
            ax.axis("off")

            rect = Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                             linewidth=1.2, edgecolor="#444", facecolor="#f9f9f9")
            ax.add_patch(rect)

            ax.text(0.06, 0.65, title, fontsize=10, color="#666", transform=ax.transAxes)
            ax.text(0.06, 0.30, value, fontsize=18, weight="bold", transform=ax.transAxes)
            ax.text(0.06, 0.15, sub, fontsize=10, color="#666", transform=ax.transAxes)


    def render_weeks_table(self, data):
        ax = self.fig.add_subplot(self.gs[4, :])
        ax.axis("off")

        weeks = data.weekly_series
        weekly_min = {item.week: item.min for item in data.weekly_min}

        headers = ["Semana", "Carga (hh:mm)", "Km", "Δ %", "Desnivel +", "Km acum.", "Desnivel acum."]

        rows = []
        km_acc = 0.0
        des_acc = 0
        for w in weeks:
            km_acc += w.km
            des_acc += w.ascent_m
            delta = "-" if w.delta_pct is None else f"{w.delta_pct:.1f}%"
            week_label = f"{w.week} ({w.week_start.strftime('%d/%m')} - {w.week_end.strftime('%d/%m')})"
            hours = minutes_to_hhmm( int(round(weekly_min.get(w.week, 0), 0)) )
            rows.append([
                week_label,
                f"{hours}",
                f"{w.km:.1f}",
                delta,
                f"{w.ascent_m:,}".replace(",", "."),
                f"{km_acc:.1f}",
                f"{des_acc:,}".replace(",", "."),
            ])

        # Me aseguro de mostrar solamente las últimas 8 semanas
        rows = rows[-8:]

        # Ordeno las semanas para ver la actual primero
        rows = list(reversed(rows))

        table = ax.table(
            cellText=rows,
            colLabels=headers,
            loc="center",
            cellLoc="center"
        )

        # Pinto el encabezado de la tabla
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor(COLOR_ENCABEZA)
                cell.set_text_props(weight="bold")
                continue
            # Color de fondo de las filas intermedias
            if row % 2 == 0:
                cell.set_facecolor(COLOR_FONDO)

        # Ajusto el ancho de las columnas
        table.scale(0.9, 1.3)
        col_widths = [0.16, 0.10, 0.08, 0.08, 0.10, 0.10, 0.10]
        for (row, col), cell in table.get_celld().items():
            if col < len(col_widths):
                cell.set_width(col_widths[col])

        table.scale(1, 1.4)
        table.auto_set_font_size(False)
        table.set_fontsize(9)


    def render_weekly_chart(self, data):
        ax = self.fig.add_subplot(self.gs[2, :])

        weeks = build_weeks_dict(data.weekly_series)
        mesocycles_weeks = {m.week for m in data.mesocycles}
        microcycle_weeks = data.microcycles
        desafios = data.desafios

        x = []
        km = []
        delta = []
        colors = []
        ascent = []

        for w in range(1, data.season.weeks + 1):
            x.append(w)
            delta.append(math.nan)          # Por ahora lo dejo fuera, tengo que pensar bien como incluirlo

            if w in weeks:
                # Semanas entrenadas
                w_km = weeks[w].km
                w_asc = weeks[w].ascent_m / 100

                km.append(w_km)
                ascent.append(w_asc)
                if microcycle_weeks[w].type != "pico_cerro":
                    colors.append(COLOR_W_HECHA)
                else:
                    colors.append(COLOR_W_CERRO)
            elif w in microcycle_weeks:
                # Semana futura planificada
                km.append(microcycle_weeks[w].meta_km)
                ascent.append(math.nan)
                if microcycle_weeks[w].type != "pico_cerro":
                    colors.append(COLOR_W_FUTURA)
                else:
                    colors.append(COLOR_F_TRAIL)
            else:
                # Semana futura sin datos
                km.append(0)
                ascent.append(math.nan)
                colors.append(COLOR_W_NONE)

        ax.bar(x, km, color=colors, alpha=0.85, label="Km")


        max_week = data.season.weeks

        all_weeks = list(range(1, max_week + 1))
        ax.set_xticks(all_weeks)
        ax.set_xlim(0.5, max_week + 0.5)

        # Dibujo el desnivel + acumulado
        ax2 = ax.twinx()
        ax2.plot(
            x,
            ascent,
            color=COLOR_W_MIN,
            linewidth=1,
            linestyle="--",
            marker="o",
            label="Desnivel + (x100 m)"
        )

        #-- - Dibujo los mesociclos y agrego sombras por zonas
        for w in mesocycles_weeks:
            ax.axvline(w + 0.5, color="gray", linestyle="--", alpha=0.4)

        mesocycles_sorted = sorted(mesocycles_weeks)

        start = 0.5
        shade = False

        for w in mesocycles_sorted:
            end = w + 0.5

            if shade:
                ax.axvspan(start, end, color=COLOR_FONDO, alpha=0.25)

            start = end
            shade = not shade

        #-- - Agrego los desafios
        y_max = max(km) * 1.1

        for week, comp in desafios.items():

            # Línea vertical roja
            ax.axvline(
                week,
                color=COLOR_DESAFIO,
                linestyle="-",
                linewidth=2,
                alpha=0.8,
                zorder=4
            )

            # Etiqueta
            label = f"{comp.name}\n{int(comp.km)} km / +{int(comp.desnivel)} m\n{comp.fecha}"

            ax.text(
                week,
                y_max,
                label,
                ha="center",
                va="bottom",
                fontsize=8,
                color=COLOR_DESAFIO,
                zorder=5
            )


        # ax.set_title("Volumen semanal")
        ax.set_xlabel("Semana")
        ax.set_ylabel("Km")
        ax2.set_ylabel("Desnivel + (x100 m)")
        ax2.set_ylim(0, max(ascent) * 1.2 if max(ascent) > 0 else 1)

        ax.grid(True, axis="y", alpha=0.3)
        ax.legend(loc="upper left")
        ax2.legend(loc="upper right")


    def render_weeks_min_chart(self, data):
        ax = self.fig.add_subplot(self.gs[3, :])

        weekly_min = data.weekly_min
        current_week = data.season.current_week

        x = []
        load = []
        rolling = []

        for item in weekly_min:
            x.append(item.week)

            if item.week <= current_week:
                load.append(item.min)
                rolling.append(item.rolling_3)
            else:
                load.append(math.nan)
                rolling.append(math.nan)

        # Carga semana
        ax.plot(
            x,
            load,
            color=COLOR_W_MIN,
            linewidth=2.0,
            marker="o",
            label="Carga semanal"
        )

        # Línea media móvil 3 semanas
        ax.plot(
            x,
            rolling,
            color=COLOR_W_HECHA,
            linewidth=1.2,
            linestyle="--",
            label="Media móvil (3 sem)"
        )

        # Zonas de posible sobrecarga
        for item in weekly_min:
            if item.week <= current_week and item.is_overload:
                ax.axvspan(
                    item.week - 0.5,
                    item.week + 0.5,
                    color=COLOR_W_INC,
                    alpha=0.25
                )


        ax.set_xlabel("Semana")
        ax.set_ylabel("Carga (min ajustados)")
        ax.set_xlim(0.5, data.season.weeks + 0.5)
        ax.set_xticks(range(1, data.season.weeks + 1))

        ax.grid(True, axis="y", alpha=0.3)

        overload_patch = Patch(
            facecolor=COLOR_W_INC,
            edgecolor='none',
            alpha=0.25,
            label="Incremento >15% semanal"
        )

        handles, labels = ax.get_legend_handles_labels()
        handles.append(overload_patch)
        ax.legend(handles=handles)
        # ax.legend()


    def render_microcycle_chart(self, data): ...

    #     ax = self.fig.add_subplot(self.gs[4, :])

    #     #-- - Calcular fecha actual (Última fecha en entrenamiento)
    #     #-- - total_dias es la cantidad de días que quiero análisar
    #     total_dias = 21
    #     days_sorted = sorted(data.days, key=lambda d: d.date)
    #     #last_day = datetime.strptime(days_sorted[-1].date, "%Y-%m-%d").date()
    #     last_day = days_sorted[-1].date

    #     #-- - Lista con la cantidad de días que quiero mostrar
    #     full_weeks = []
    #     for i in range(total_dias):
    #         day_date = last_day - timedelta(days=i)
    #         full_weeks.append(day_date)
    #     # Orden cronologico
    #     full_weeks = list(reversed(full_weeks))

    #     #-- - Indexo days para realizar busquemas más rapidas
    #     days_index = {d.date: d for d in data.days}


    #     x_labels = []
    #     minutes = []
    #     km = []
    #     sessions_count = []
    #     hr_avg = []
    #     hr_max = []

    #     for day_date in full_weeks:
    #         # x_labels.append(day_date.strftime("%a")[0])  # L, M, X...
    #         x_labels.append(f"{DIAS_ES[day_date.weekday()]}\n{day_date.strftime('%d/%m')}")

    #         if day_date in days_index:
    #             sessions = days_index[day_date].sessions

    #             total_min = sum(s.time_min for s in sessions)
    #             total_km = sum(s.distance_km for s in sessions)
    #             total_sessions = len(sessions)

    #             if total_min > 0:
    #                 weighted_hr = sum(s.avg_hr * s.time_min for s in sessions) / total_min
    #             else:
    #                 weighted_hr = 0

    #             max_hr = max((s.max_hr for s in sessions), default=0)

    #         else:
    #             total_min = 0
    #             total_km = 0
    #             total_sessions = 0
    #             weighted_hr = 0
    #             max_hr = 0

    #         minutes.append(total_min)
    #         km.append(total_km)
    #         sessions_count.append(total_sessions)
    #         hr_avg.append(weighted_hr)
    #         hr_max.append(max_hr)

    #     x = range(len(full_weeks))

    #     # --- Barras minutos ---
    #     bars = ax.bar(x, minutes, alpha=0.7)

    #     # Mostrar número de sesiones sobre cada barra
    #     for i, val in enumerate(minutes):
    #         if val > 0:
    #             ax.text(
    #                 i,
    #                 val + max(minutes) * 0.03,
    #                 str(sessions_count[i]),
    #                 ha="center",
    #                 fontsize=9,
    #                 weight="bold"
    #             )

    #     ax.set_ylabel("Minutos")
    #     ax.set_xticks(x)
    #     ax.set_xticklabels(x_labels)
    #     ax.set_xlabel("Día")

    #     # --- Línea KM ---
    #     ax2 = ax.twinx()
    #     ax2.plot(
    #         x,
    #         km,
    #         linewidth=2,
    #         marker="o",
    #         label="Km"
    #     )
    #     ax2.set_ylabel("Km")

    #     ax.grid(True, axis="y", alpha=0.3)

    #     handles1, labels1 = ax.get_legend_handles_labels()
    #     handles2, labels2 = ax2.get_legend_handles_labels()

    #     ax.legend(handles1 + handles2,
    #             labels1 + labels2,
    #             loc="upper left")


    def finalize(self):
        if self.mode == "imagen":
            plt.savefig(self.output_path, dpi=150)
            print(f"Dashboard generado: {self.output_path}")
        else:
            plt.show()

        plt.close()


def minutes_to_hhmm(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d} h {minutes:02d} m"


def build_weeks_dict(weeks):
    r = {}

    for w in weeks:
        r[w.week] = w

    return r
