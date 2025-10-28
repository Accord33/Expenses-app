import flet as ft


# Factory that returns an event handler bound to a page instance.
def make_handle_change(page: ft.Page):
    def handle_change(e: ft.ControlEvent):
        # e.data is the selected index (string or int depending on platform)
        print(f"selected_index: {e.data}")
        page.open(ft.SnackBar(ft.Text(f"segment {int(e.data) + 1} chosen")))
        # Note: this generic handler adds a SnackBar. Avoid modifying page.controls here
        # because view-specific UI should be updated by local handlers.
        page.update()

    return handle_change


def main(page: ft.Page):
    def navigatioin_bar_func():
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EDIT, label="入力"),
                ft.NavigationBarDestination(icon=ft.Icons.PIE_CHART, label="レポート"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Input",
                ),
            ],
            on_change=lambda e: page.go(f"/view{e.control.selected_index + 1}"),
        )

    def create_view1():
        # Create a Text control that will display the selected segment label
        selected_control = ft.Column()

        def on_segment_change(e: ft.ControlEvent):
            try:
                idx = int(e.data)
            except Exception:
                idx = 0
            if idx == 0:
                selected_control.controls = [ft.Text("支出")]
            else:
                selected_control.controls = [ft.Text("収入")]
            page.update()

        return ft.View(
            "/view1",
            [
                ft.AppBar(title=ft.Text("View 1")),
                navigatioin_bar_func(),
                ft.Column(
                    [
                        ft.CupertinoSlidingSegmentedButton(
                            selected_index=1,
                            thumb_color=ft.Colors.BLUE_400,
                            on_change=on_segment_change,
                            controls=[
                                ft.Text("支出"),
                                ft.Text("収入"),
                            ],
                        ),
                        ft.Container(height=12),
                        selected_control,
                    ]
                ),
            ],
        )

    def create_view2():
        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    26,
                    color=ft.Colors.BLUE,
                    radius=70,
                    title="25%",
                ),
                ft.PieChartSection(
                    24,
                    color=ft.Colors.YELLOW,
                    radius=70,
                ),
                ft.PieChartSection(
                    25,
                    color=ft.Colors.PINK,
                    radius=70,
                ),
                ft.PieChartSection(
                    25,
                    color=ft.Colors.GREEN,
                    radius=70,
                ),
            ],
            center_space_radius=50,
        )

        def test():
            return ft.Text("test")

        return ft.View(
            "/view2",
            [
                ft.AppBar(title=ft.Text("View 2")),
                navigatioin_bar_func(),
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text("支出"),
                                ft.Text(
                                    "-1000円",
                                    color=ft.Colors.RED,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            [
                                ft.Text("収入"),
                                ft.Text(
                                    "+2000円",
                                    color=ft.Colors.BLUE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                ft.Divider(height=0),
                ft.Row(
                    [
                        ft.Text("収支"),
                        ft.Text(
                            "+0円", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                ft.Divider(height=0),
                ft.Tabs(
                    tabs=[
                        ft.Tab(
                            text="　　　　支出　　　　",
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        chart,
                                        ft.ListTile(
                                            title=ft.Row(
                                                [
                                                    ft.Text("食費"),
                                                    ft.Text("1000円"),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                            trailing=ft.Icon(
                                                ft.Icons.ARROW_FORWARD_IOS
                                            ),
                                            leading=ft.Icon(ft.Icons.FASTFOOD),
                                            on_click=lambda e: print("ListTile clicked"),
                                        ),
                                        ft.Divider(height=0),
                                        ft.ListTile(
                                            title=ft.Row(
                                                [
                                                    ft.Text("交際費"),
                                                    ft.Text("1000円"),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            ),
                                            trailing=ft.Icon(
                                                ft.Icons.ARROW_FORWARD_IOS
                                            ),
                                            leading=ft.Icon(ft.Icons.WINE_BAR),
                                        ),
                                    ]
                                )
                            ),
                        ),
                        ft.Tab(
                            text="　　　　収入　　　　",
                            content=ft.Text("収入タブの内容がここに表示されます"),
                        ),
                    ],
                    tab_alignment=ft.TabAlignment.CENTER,
                ),
                ft.Text("チャートの説明文や凡例などをここに追加できます"),
            ],
        )

    def create_view3():
        return ft.View(
            "/view3",
            [
                ft.AppBar(title=ft.Text("View 3")),
                ft.ElevatedButton("Go to View 1", on_click=lambda _: page.go("/view1")),
                navigatioin_bar_func(),
            ],
        )

    def route_change(handler):
        page.views.clear()
        if handler.route == "/view1":
            page.views.append(create_view1())
        elif handler.route == "/view2":
            page.views.append(create_view2())
        elif handler.route == "/view3":
            page.views.append(create_view3())
        page.update()

    page.on_route_change = route_change
    page.go("/view2")  # 初期表示としてView1を設定


ft.app(target=main)
