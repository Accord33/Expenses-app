import flet as ft


def create_navigation_bar(page: ft.Page):
    """ナビゲーションバーを作成する"""
    return ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EDIT, label="入力"),
            ft.NavigationBarDestination(icon=ft.Icons.PIE_CHART, label="レポート"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Input",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CAMERA_ALT,
                label="読込",
            ),
        ],
        on_change=lambda e: page.go(f"/view{e.control.selected_index + 1}"),
    )
