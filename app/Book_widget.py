import flet as ft
from multitool import shorter, to_next_line

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
