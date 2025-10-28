import flet as ft


def create_category_detail(page: ft.Page, category: str):
    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=40,
                        width=40,
                        color=ft.Colors.ORANGE,
                        # tooltip="Apple",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=100,
                        width=40,
                        color=ft.Colors.ORANGE,
                        # tooltip="Blueberry",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=30,
                        width=40,
                        color=ft.Colors.ORANGE,
                        # tooltip="Cherry",
                        border_radius=0,
                    ),
                ],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=60,
                        width=40,
                        color=ft.Colors.ORANGE,
                        # tooltip="Orange",
                        border_radius=0,
                    ),
                ],
            ),
        ],
        border=ft.border.all(1, ft.Colors.GREY_400),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0, label=ft.Container(ft.Text("7月"), padding=10)
                ),
                ft.ChartAxisLabel(
                    value=1, label=ft.Container(ft.Text("8月"), padding=10)
                ),
                ft.ChartAxisLabel(
                    value=2, label=ft.Container(ft.Text("9月"), padding=10)
                ),
                ft.ChartAxisLabel(
                    value=3, label=ft.Container(ft.Text("10月"), padding=10)
                ),
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
    )

    def pop(page: ft.Page):
        page.views.pop()
        page.update()
        page.go("/view2")
        

    """カテゴリー詳細画面を作成する"""
    return ft.View(
        "/category_detail",
        [
            ft.AppBar(
                leading=ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK_IOS),
                    on_click=lambda e: pop(page),
                ),
                title=ft.Text(
                    f"{category} 2000円",
                ),
            ),
            chart,
            ft.Column(
                [
                    ft.ListTile(
                        title=ft.Row(
                            [
                                ft.Text("交際費"),
                                ft.Text("1000円"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS),
                        leading=ft.Icon(ft.Icons.WINE_BAR),
                    ),
                ]
            ),
        ],
    )
