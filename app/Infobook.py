import flet as ft
from multitool import shorter, to_next_line,sort
import json
from search import parse_books, preload_covers
    
def load_books():
    """Актуальный books_data.json"""
    with open("books_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


class BookWidget:
    def __init__(self, page, books, main_page, search_res):
        self.page = page
        self.books = books
        self.main_page = main_page
        self.search_res = search_res
        self.width = 270
        self.height = 500

    def handle_click(self, e, book):
        self.page.launch_url(book["links"].split("http://books.google.co.uz")[-1], web_window_name="_self")
        self.page.title = book["title"]
        self.main_page.controls.clear()
        self.search_res.controls.clear()
        self.main_page.controls.append(
        ft.Column(
    [
        ft.Row([ft.Text(book["title"], weight="bold")]),
        ft.Row(
            [
                ft.Image(
                    src_base64=book["cover_b64"],
                    width=200,
                    height=270,
                    fit=ft.ImageFit.CONTAIN
                ),
                ft.Container(
                    content=ft.Text(to_next_line(book["description"], 140)), bgcolor="#91AFE4",border_radius=20, padding=30)]),
        ft.Row([ft.Text(f"{book['rating']}⭐ from {book['rating_count']}")])
    ]
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
                                            src_base64=book["cover_b64"],
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
                    border_radius=10,
                    on_click=lambda e, b=book: self.handle_click(e, b),
                )
            )
        return controls


def Main(page: ft.Page):
    page.title = "InfoBook"
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = "light"
    page.assets_dir = "assets"

    username = ft.TextField(label="Username", width=250)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=250)
    buttons_row = ft.Row(alignment=ft.MainAxisAlignment.END)
    main_page = ft.GridView(
        expand=1, runs_count=6, max_extent=250, child_aspect_ratio=0.45,
        spacing=50, run_spacing=50
    )
    search_results = ft.Column()



    def show_books(books=load_books()):
        widgets = BookWidget(page, books, main_page, search_results)
        main_page.controls.clear()
        main_page.controls.extend(widgets.container())
        page.update()

    def analyse(e):
        page.open(ft.SnackBar(ft.Text("THERE IS NO LOGIC NOW YOU ,PLEASE WAIT")))

    def on_logo_click(e):
        search_results.controls.clear()
        show_books(load_books())
    
    def on_search_click(e):
        query = search_input.value.strip()
        search_results.controls.clear()

        if query:
            search_results.controls.append(
                ft.Row(
                    [ft.Text("Your search results for:"),
                    ft.Text(query, italic=True, color=ft.Colors.BLUE_600, selectable=True)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            books = preload_covers(parse_books(query=query, max_results=20))

            if load_books():
                show_books(books)
            else:
                main_page.controls.clear()
                main_page.controls.append(ft.Text("No books found."))
        search_input.value = ""
        page.update()

    search_input = ft.TextField(label="Search books...", width=300)
    show_books()

    def on_droplist_change(e):
        dropval = sort_button.value
        show_books(sort(load_books(), dropval))

    def do_login():
        if username.value == "admin" and password.value == "admin":
            page.open(ft.SnackBar(ft.Text("Login Successful!")))
            page.close(login_dlg)
            buttons_row.controls.insert(
                0, ft.ElevatedButton("Parse Books", color=ft.Colors.BLUE, on_click=analyse)
            )
        else:
            page.open(ft.SnackBar(ft.Text("Successful Login!")))
            page.close(login_dlg)
        page.update()

    login_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Login"),
        content=ft.Column([username, password], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: page.close(login_dlg)),
            ft.ElevatedButton("Login", on_click=lambda e: do_login()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    theme_button = ft.ElevatedButton("🌙 / ☀️", on_click=lambda e: (
        setattr(page, "theme_mode", "dark" if page.theme_mode == "light" else "light"),
        page.update()
    ))

    login_button = ft.ElevatedButton("Login", on_click=lambda e: page.open(login_dlg))
    buttons_row.controls.extend([theme_button, login_button])

    sort_button=ft.Dropdown(
    options=[
        ft.dropdown.Option("title"),
        ft.dropdown.Option("date"),
        ft.dropdown.Option("jenre"),
    ]
    , on_change=on_droplist_change, width=150
)

    page.add(
        ft.Column(
            [
                buttons_row,
                ft.Row(
                    [
                        ft.TextButton(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.MENU_BOOK_OUTLINED, size=30),
                                    ft.Text("InfoBook", size=30)
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            on_click=on_logo_click,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
                            width=200,
                            height=40,
                        ),

                        ft.Container(width=200),         

                        search_input,
                        ft.IconButton(
                            ft.Icons.SAVED_SEARCH,
                            on_click=on_search_click,
                            tooltip="Search"
                        ),
                        ft.Container(width=200),
                        sort_button,
                        
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                search_results,
                main_page,
            ]
        )
    )


ft.app(target=Main, view=None)