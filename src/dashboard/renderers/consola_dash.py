from src.dashboard.renderers.base import DashboardRenderer


class ConsolaRenderer(DashboardRenderer):

    def render_header(self, data):
        season = data.season
        print("\nDashboard entrenamiento\n")
        print(f"Temporada : {season.name} ({season.code})")
        print(f"Semana actual: {season.current_week}")
        print(f"Rango: {season.week_start} - {season.week_end}")


    def render_cards(self, data):
        cards = data.summary_cards

        print("\nResumen acumulado:\n")
        print(f"Km totales     : {cards.total_km}")
        print(f"Desnivel +     : {cards.total_ascent_m} m")
        print(f"Tiempo total   : {cards.total_time_min} min")
        print(f"Sesiones       : {cards.total_sessions}")


    def render_weeks_table(self, data):
        print("\nResumen semanal:\n")

        header = f"{'Semana':<8} {'Km':<8} {'Δ%':<6} {'Ses':<5} {'Asc m':<8}"
        print(header)
        print("-" * len(header))

        for w in data.weekly_series:
            delta = "-" if w.delta_pct is None else f"{w.delta_pct:+.1f}"
            print(
                f"{w.week:<8} "
                f"{w.km:<8.2f} "
                f"{delta:<6} "
                f"{w.sessions:<5} "
                f"{w.ascent_m:<8}"
            )


    def render_weekly_chart(self, data):
        print("\nVolumen semanal (km):\n")

        weeks = data.weekly_series
        microcycles = {m.week for m in data.microcycles}

        if not weeks:
            print("(sin datos)")
            return

        max_km = max(w.km for w in weeks)
        scale = 40 / max_km if max_km > 0 else 1

        for w in weeks:
            bar = "█" * int(w.km * scale)
            marker = "|" if w.week in microcycles else " "

            delta = "-" if w.delta_pct is None else f"{w.delta_pct:+.1f}"

            print(
                f"{w.week:>2} {marker} {bar:<40} {w.km:>5.1f} km  Δ {delta}"
            )


    def finalize(self):
        print("\n-- Dashboard generado (consola) --\n")
