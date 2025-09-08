import flet as ft
from multitool import shorter, search
import json

with open("books_data.json", "r", encoding="utf-8") as f:
    books_data = json.load(f)


class BookWidget:
    def __init__(self, page, books, main_page, search_res):
        self.page = page
        self.books = books
        self.main_page = main_page
        self.search_res = search_res
        self.width = 270
        self.height = 500
    def handle_click(self, e, book):
        self.page.launch_url(book["links"].split("https://www.litres.ru")[-1], web_window_name="_self")
        self.page.title = book["title"]

        self.main_page.controls.clear()
        self.search_res.controls.clear()
        self.main_page.controls.append(
            ft.Column(
                [
                    ft.Row([ft.Text(book["title"], size=16, weight=ft.FontWeight.BOLD)]),
                    ft.Row([ft.Image(src=book["cover"], width=200, height=270, fit=ft.ImageFit.CONTAIN)]),
                    ft.Row([ft.Text(book.get("author", ""))]),
                    ft.Row([ft.Text(book.get("price", ""))]),
                    ft.Row([ft.Text(f"{book['rating']}⭐ из {book['rating_count']}")]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.update()

    def container(self):
        controls = []
        for book in self.books:
            controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Image(
                                        src=book["cover"],
                                        fit=ft.ImageFit.CONTAIN,
                                        width=200,
                                        height=270,
                                        error_content=ft.Image(
                                            "NotFound.jpg",
                                            width=200,
                                            height=270,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.BOOK),
                                title=ft.Text(shorter(book["title"])),
                                subtitle=ft.Column([ft.Text(book["type"]), ft.Text(book["author"])]),
                                bgcolor="#3C8060",
                            ),
                            ft.Row(
                                [ft.Text(book["price"], weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                    bgcolor="#3C8060",
                    width=self.width,
                    height=self.height,
                    ink=True,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.BLACK12,
                        offset=ft.Offset(2, 2)
                    ),
                    border_radius = 10,
                    on_click=lambda e, b=book: self.handle_click(e, b),
                )
            )
        return controls


def Main(page: ft.Page):
    page.title = "InfoBook"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS
    page.assets_dir = "assets"
    page.theme_mode = "light"


    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    
    theme_button = ft.ElevatedButton(
            text="🌙 / ☀️",
            on_click=toggle_theme
        )

    main_page = ft.GridView(
        expand=1,
        runs_count=6,
        max_extent=250,
        child_aspect_ratio=0.45,
        spacing=50,
        run_spacing=50,
    )
    search_results = ft.Column()

    def show_books(lst):
        books_widgets = BookWidget(page, lst, main_page, search_results)
        main_page.controls.clear()
        main_page.controls.extend(books_widgets.container())
        page.update()

    def on_logo_click(e):
        search_results.controls.clear()
        show_books(books_data)
        if page.route not in ["/", ""]:
            page.title = "InfoBook"
            page.launch_url("/", web_window_name="_self")
        page.update()

    def on_search_click(e):
        query = search_input.value.strip()
        search_results.controls.clear()

        if query:
            search_results.controls.append(
                ft.Row(
                    [
                        ft.Text("Your search results for:"),
                        ft.Text(query, italic=True, color=ft.Colors.BLUE_600, selectable=True),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            found_books = search(books_data, query)
            if found_books:
                show_books(found_books)
            else:
                main_page.controls.clear()
                main_page.controls.append(ft.Text("No books found."))

        search_input.value = ""
        page.update()

    search_input = ft.TextField(label="Search books...", width=300)

    show_books(books_data)

    page.add(
        ft.Column(
            [
            ft.Row(
                [theme_button],
                alignment=ft.MainAxisAlignment.END
            ),
                ft.Row(
                    [
                        ft.TextButton(
    content = ft.Row(
        [
            ft.Icon(ft.Icons.MENU_BOOK_OUTLINED, size=30),
            ft.Text("InfoBook", size=30),                   
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    ),
    on_click=on_logo_click,
    style=ft.ButtonStyle(
        bgcolor=ft.Colors.TRANSPARENT
    ),
    width=200,
    height=40
),
                        ft.Container(width=400),
                        search_input,
                        ft.IconButton(ft.Icons.SAVED_SEARCH, on_click=on_search_click, tooltip="Search"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                search_results,
                main_page,
            ]
        )
    )
    page.update()


ft.app(target=Main, view=ft.WEB_BROWSER)
