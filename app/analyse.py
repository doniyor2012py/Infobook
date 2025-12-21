import flet as ft
from search import total_books

def piechart():
    """Creates a pie chart of book genres"""
    genres = ["fantastic", "romance", "science", "horror", "sport"]
    results = {g: total_books(f"subject:{g}") for g in genres}

    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    hover_title_style = ft.TextStyle(
        size=16,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
    )
    normal_badge_size = 40
    hover_badge_size = 50

    def badge(icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.Colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.Colors.WHITE,
        )

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    icons = [
        ft.Icons.PRECISION_MANUFACTURING_ROUNDED,
        ft.Icons.FAVORITE,
        ft.Icons.SCIENCE,
        ft.Icons.TAG_FACES_ROUNDED,
        ft.Icons.SPORTS_FOOTBALL,
    ]
    colors = [ft.Colors.BLUE, ft.Colors.RED, ft.Colors.YELLOW, ft.Colors.PURPLE, ft.Colors.GREEN]

    sections = []
    for (genre, count), icon, color in zip(results.items(), icons, colors):
        sections.append(
            ft.PieChartSection(
                value=count,
                title=f"{genre.capitalize()} {count}",
                title_style=normal_title_style,
                color=color,
                radius=normal_radius,
                badge=badge(icon, normal_badge_size),
                badge_position=0.98,
            )
        )

    chart = ft.PieChart(
        sections=sections,
        sections_space=0,
        center_space_radius=0,
        on_chart_event=on_chart_event,
        expand=True,
    )

    return chart
