import flet as ft
from search import total_books

def piechart():
    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(
        size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
    )
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

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                total_books("subject:fantastic"),
                title=f"Fantastic  {total_books('subject:fantastic')}",
                title_style=normal_title_style,
                color=ft.Colors.BLUE,
                radius=normal_radius,
                badge=badge(ft.Icons.PRECISION_MANUFACTURING_ROUNDED, normal_badge_size),
                badge_position=0.98,
            ),
            ft.PieChartSection(
                total_books("subject:romance"),
                title=f"Romance  {total_books('subject:romance')}",
                title_style=normal_title_style,
                color=ft.Colors.RED,
                radius=normal_radius,
                badge=badge(ft.Icons.FAVORITE, normal_badge_size),
                badge_position=0.98,
            ),
            ft.PieChartSection(
                total_books("subject:science"),
                title=f"Science  {total_books('subject:science')}",
                title_style=normal_title_style,
                color=ft.Colors.YELLOW,
                radius=normal_radius,
                badge=badge(ft.Icons.SCIENCE, normal_badge_size),
                badge_position=0.98,
            ),
            ft.PieChartSection(
                total_books("subject:horror"),
                title=f"Horror  {total_books('subject:horror')}",
                title_style=normal_title_style,
                color=ft.Colors.PURPLE,
                radius=normal_radius,
                badge=badge(ft.Icons.TAG_FACES_ROUNDED, normal_badge_size),
                badge_position=0.98,
            ),
            ft.PieChartSection(
                total_books("subject:sport"),
                title=f"Sport  {total_books('subject:sport')}",
                title_style=normal_title_style,
                color=ft.Colors.GREEN,
                radius=normal_radius,
                badge=badge(ft.Icons.SPORTS_FOOTBALL, normal_badge_size),
                badge_position=0.98,
            ),
        ],
        sections_space=0,
        center_space_radius=0,
        on_chart_event=on_chart_event,
        expand=True,
    )

    return chart
