import flet as ft
from components.navigation import create_navigation_bar


def create_view3(page: ft.Page):
    """View 3: ブックマーク画面を作成する"""
    return ft.View(
        "/view3",
        [
            ft.AppBar(title=ft.Text("View 3")),
            ft.ElevatedButton("Go to View 1", on_click=lambda _: page.go("/view1")),
            create_navigation_bar(page),
        ],
    )
