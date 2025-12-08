import flet as ft
from multitool import shorter, to_next_line,sort
import json
from search import parse_books, preload_covers
import os
import pathlib
from bot import support_message

print("📂 Files in current dir:", os.listdir())
print("📂 Full path:", os.path.abspath(__file__))


def load_books():
    """Загружает JSON файл. Сейчас это - books_data.json для главной странице"""
    try:
        BASE_DIR = pathlib.Path(__file__).parent
        file_path = BASE_DIR / "books_data.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []




class BookWidget:
    """===================Класс который включает в себя=============================

        - Defult характеристики карточек для книг для главной страницы, такие как:
            Из books_data.json:
                - Название книги ~ title
                - Автор книги ~ author
                - Год опубликование ~ date
                - Цена ~ price
                - Обложка ~  cover (cover_b64 для использования)
            - Переменные контейнера карточки в главной странице:
                - Ширина карточки ~ self.width
                - Высота карочки ~ self.height
                - Результат поиск ~ search_res

        - Функции в странице книги (все из books_data.json): 
            - Описание книги 
            - Обложка книги
            - Рейтинг книги
            - Кнопка перехода на сайт с книгой
    =================================================================================

    ```````````````````````````````Функции```````````````````````````````````````````
    __init__ :self, page, books, main_page, search_res -> Определяет переменные через self + self.width ~ 270; self.height ~ 500
    button_go_to_site_click : e, book -> Отпровляет пользовотеля на сайт с книгой
    handle_click : e, books -> Удаляет книги и "открывает" страницу книги (и изменяет имя страницы на название книги с описанием), обложкой,названием и автором книги, рейтингом книги и кнопкй на сам сайт с книгой
    container -> Создает карточки для всех books с обложкой, рейтингом, ценой, названием и автором книги при нажатии вызывает handle_click и возвращает функция controls что является ft.Container

    `````````````````````````````````````````````````````````````````````````````````

    """
    def __init__(self, page, books, main_page, search_res):
        self.page = page
        self.books = books
        self.main_page = main_page
        self.search_res = search_res
        self.width = 270
        self.height = 500
    
    def button_go_to_site_click(self, e, book):
        self.page.launch_url(book["links"], web_window_name="_self")
    def handle_click(self, e, book):
        self.page.title = book["title"]
        self.main_page.controls.clear()
        self.search_res.controls.clear()
        self.main_page.controls.append(
        ft.Column([
    
            ft.Row([ft.Text(book["title"], weight="bold")]),
            ft.Row([
                
                    ft.Image(
                        src_base64=book["cover_b64"],
                        width=200,
                        height=270,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    ft.Container(
                        content=ft.Text(to_next_line(book["description"], 140)), 
                        bgcolor="#91AFE4",
                        border_radius=20, 
                        padding=30
                        )
            ]),

            ft.Row([
                ft.Text(f"{book['rating']}⭐ from {book['rating_count']}")
            ]),

            ft.Row([
                ft.TextButton("Go to the site of book",
                    icon="bookmarks",
                    icon_color="green600",
                    on_click=lambda e: self.button_go_to_site_click(e, book)
                )
            ])
        ])
    )
        self.page.update()
    def container(self) -> ft.Container:
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
    sort_books = load_books()
    #__________________________________SUPPOORT____________________________________

    support_username = ft.TextField(label="Ваш Юзернейм", width=300)
    support_msg = ft.TextField(label="Сообщение", multiline=True, width=300, height=100)
    support_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("💬 Поддержка"),
        content=ft.Column([
            ft.Text("Если у вас есть идеи, напишите нам:"),
            support_username,
            support_msg,
        ]),
        actions=[
            ft.TextButton("Отмена", on_click=lambda e: page.close(support_dialog)),
            ft.ElevatedButton("Отправить", 
            on_click=lambda e: (
                page.open(ft.SnackBar(ft.Text("Сообщение отправлено!"))),
                support_message(f"{support_username.value if support_username else 'anonym'} : {support_msg.value}"),
                print(support_username.value if support_username else "anonym"),
                print(support_msg.value)
            )),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.CONTACT_SUPPORT_OUTLINED,
        bgcolor=ft.Colors.BLUE,
        tooltip="Contact Support",
        on_click=lambda e: page.open(support_dialog),
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.END_FLOAT
    
    
    #__________________Registration labels____________________________
    username = ft.TextField(label="Username", width=250)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=250)


    #_____________________Main page header and main content varibles____________________
    buttons_row = ft.Row(alignment=ft.MainAxisAlignment.END)
    main_page = ft.GridView(
        expand=1, runs_count=6, max_extent=250, child_aspect_ratio=0.45,
        spacing=50, run_spacing=50
    )
    search_results = ft.Column()



    def show_books(books=load_books()):
        """
        - Clears main page contents
        - Calls BookWidget class to generate new books
        """

        widgets = BookWidget(page, books, main_page, search_results)
        main_page.controls.clear()
        main_page.controls.extend(widgets.container())
        page.update()

    def analyse(e):
        """ TODO: Anylyse Logic """
        page.open(ft.SnackBar(ft.Text("THERE IS NO LOGIC NOW YOU ,PLEASE WAIT")))

    def on_logo_click(e):
        """Go to main page on logo click"""
        page.title = "InfoBook"
        search_results.controls.clear()
        show_books(load_books())
    
    def on_search_click(e):
        """Search book with GoogleBooks API. In the func calls another funcs like show_books, preloud_covers, parse_books and varible ~ sort_books"""
        query = search_input.value.strip()
        search_results.controls.clear()
        nonlocal sort_books
        if query:
            search_results.controls.append(
                ft.Row(
                    [ft.Text("Your search results for:"),
                    ft.Text(query, italic=True, color=ft.Colors.BLUE_600, selectable=True)],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            sort_books = preload_covers(parse_books(query=query, max_results=20))
            
            if sort_books:
                show_books(sort_books)
            else:
                main_page.controls.clear()
                main_page.controls.append(ft.Text("No books found."))
        search_input.value = ""
        page.update()

    search_input = ft.TextField(label="Search books...", width=300)
    show_books()

    def on_droplist_change(e):
        """Sorts books on droplist change"""
        dropval = sort_button.value
        show_books(sort(sort_books, dropval))

    def do_login():
        """Logic of login"""
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

    #__________LOGIN Alert Dialog_________________
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

    #___________Header___________________________
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
        ,
        border_radius=5,
        focused_border_color=ft.Colors.BLUE_200,
        label="Sort...",
        on_change=on_droplist_change,
        width=150
)
    #________________Adding all in main page__________________________
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