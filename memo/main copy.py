import flet as ft


def main(page: ft.Page):
    def create_view1():
        return ft.View(
            "/view1",
            [
                ft.AppBar(title=ft.Text("View 1")),
                ft.ElevatedButton("Go to View 2", on_click=lambda _: page.go("/view2")),
            ],a
        )

    def create_view2():
        return ft.View(
            "/view2",
            [
                ft.AppBar(title=ft.Text("View 2")),
                ft.ElevatedButton("Go to View 1", on_click=lambda _: page.go("/view1")),
            ],
        )

    def route_change(handler):
        page.views.clear()
        if handler.route == "/view1":
            page.views.append(create_view1())
        elif handler.route == "/view2":
            page.views.append(create_view2())
        page.update()

    page.on_route_change = route_change
    page.go("/view1")  # 初期表示としてView1を設定


ft.app(target=main)
