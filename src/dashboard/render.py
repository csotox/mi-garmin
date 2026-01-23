def render_header(season):
    print("\nDashboard entrenamiento\n")
    print(f"Temporada : {season.name} ({season.code})")
    print(f"Semana actual: {season.current_week}")
    print(f"Rango: {season.week_start} - {season.week_end}")


def render_cards(cards):
    print("\nResumen acumulado:\n")

    print(f"Km totales     : {cards.total_km}")
    print(f"Desnivel +     : {cards.total_ascent_m} m")
    print(f"Tiempo total   : {cards.total_time_min} min")
    print(f"Sesiones       : {cards.total_sessions}")


def render_weeks_table(weeks):
    print("\nResumen semanal:\n")

    header = f"{'Semana':<8} {'Km':<8} {'Δ%':<6} {'Ses':<5} {'Asc m':<8}"
    print(header)
    print("-" * len(header))

    for w in weeks:
        delta = "-" if w.delta_pct is None else f"{w.delta_pct:+.1f}"
        print(f"{w.week:<8} {w.km:<8.2f} {delta:<6} {w.sessions:<5} {w.ascent_m:<8}")


def render_weekly_chart(weeks, microcycles):
    print("\nVolumen semanal (km):\n")

    max_km = max(w.km for w in weeks)
    scale = 40 / max_km

    micro_weeks = {m.week for m in microcycles}

    for w in weeks:
        bar = "█" * int(w.km * scale)
        marker = "|" if w.week in micro_weeks else " "
        print(f"{w.week:>2} {marker} {bar} {w.km:.1f} km")
