import flet as ft
from components.navigation import create_navigation_bar


def create_view2(page: ft.Page):
    """View 2: レポート画面を作成する"""
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

    return ft.View(
        "/view2",
        [
            ft.AppBar(title=ft.Text("View 2")),
            create_navigation_bar(page),
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
                                        on_click=lambda e: page.go("/category_detail?category=food"),
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
                                        on_click=lambda e: page.go("/category_detail?category=entertainment"),
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
