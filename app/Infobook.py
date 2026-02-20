import flet as ft
from multitool import sort, load_books
from Book_widget import BookWidget
import json
from search import parse_books, preload_covers, total_books
import os
from bot import support_message
from analyse import piechart

print("📂 Files in current dir:", os.listdir())
print("📂 Full path:", os.path.abspath(__file__))





def Main(page: ft.Page):
    analytics = "<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <!-- Privacy-friendly analytics by Plausible -->
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-Q_jj32-309OTnnqJrvPZ9.js"></script>
<script>
  window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
  plausible.init()
</script>


</head>
<body></body>
</html>
"
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



    def show_books(books=None):
        """
        - Clears main page contents
        - Calls BookWidget class to generate new books
        """

        if books is None:

            books = load_books()

        widgets = BookWidget(page, books, main_page, search_results)
        main_page.controls.clear()
        main_page.controls.extend(widgets.container())
        page.update()

    def analyse(e):
        """ TODO: Anylyse Logic """
        main_page.clean()
        main_page.controls.append(piechart())
        page.update()


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
                0, ft.ElevatedButton("Books Analyse", color=ft.Colors.BLUE, on_click=analyse)
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
    page.add(analytics)
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