import flet as ft
from components.navigation import create_navigation_bar


# カテゴリ定義
EXPENSE_CATEGORIES = ["食費", "交通費", "娯楽費", "日用品"]
INCOME_CATEGORIES = ["給与", "副業", "ボーナス", "その他"]


class ContentButton:
    def __init__(self, page: ft.Page, name_list: list[str]):
        self.page = page
        self.button_list = []
        self.name_list = name_list
        self.focus_index = 0

        for i, name in enumerate(self.name_list):
            self.button_list.append(
                ft.Container(
                    content=ft.CupertinoButton(
                        content=ft.Text(
                            f"{name}",
                            # ダークモードの時は白、ライトモードの時は黒
                            color=ft.Colors.WHITE
                            if page.theme_mode == ft.ThemeMode.DARK
                            else ft.Colors.BLACK,
                        ),
                        opacity_on_click=0.3,
                        on_click=lambda e, idx=i: self.focus_button(idx),
                    ),
                    # デフォルトのボーダー色（非選択時）
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=10,
                )
            )

        self.focus_button(self.focus_index)

    def focus_button(self, index: int):
        # 前回選択されていたボタンのボーダーをデフォルトに戻す
        self.button_list[self.focus_index].border = ft.border.all(1, ft.Colors.OUTLINE)
        self.focus_index = index
        # 選択されたボタンのボーダーを青色に
        self.button_list[index].border = ft.border.all(2, ft.Colors.BLUE)
        self.page.update()

    def get_focused_content(self):
        return self.name_list[self.focus_index]

    def get_category_index(self, category_name: str) -> int | None:
        """カテゴリ名からインデックスを取得"""
        try:
            return self.name_list.index(category_name)
        except ValueError:
            return None


def create_view1(page: ft.Page):
    selected_control = ft.Column()

    # 入力フィールドの参照を保持
    price_field = ft.TextField(
        adaptive=True,
        label="金額",
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
    )
    date_field = ft.TextField(
        adaptive=True,
        label="日付:YYYYMMDD",
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
    )

    # 支出用と収入用のContentButtonを作成
    expense_button = ContentButton(page, EXPENSE_CATEGORIES)
    income_button = ContentButton(page, INCOME_CATEGORIES)
    
    # 現在アクティブなContentButtonを管理
    current_button = expense_button
    
    # セグメントボタンの参照を保持
    segment_button = ft.CupertinoSlidingSegmentedButton(
        selected_index=0,
        thumb_color=ft.Colors.BLUE_400,
        on_change=None,  # 後で設定
        controls=[
            ft.Text("　　支出　　"),
            ft.Text("　　収入　　"),
        ],
    )

    def apply_analysis_result():
        """セッションから解析結果を取得して適用"""
        result = page.session.get("analysis_result")
        if not result:
            return
        
        # フィールドに値を設定
        price_field.value = result.get("price", "")
        date_field.value = result.get("date", "")

        # 収入/支出の判定
        result_type = result.get("type", "expense")  # デフォルトは支出
        category = result.get("category", "")
        
        # セグメントボタンとContentButtonを切り替え
        if result_type == "income":
            segment_button.selected_index = 1
            active_button = income_button
        else:
            segment_button.selected_index = 0
            active_button = expense_button
        
        # カテゴリを設定（動的に検索）
        if category:
            category_index = active_button.get_category_index(category)
            if category_index is not None:
                active_button.focus_button(category_index)
        
        # セグメント変更を反映
        on_segment_change_internal(segment_button.selected_index)
        
        # セッションをクリア
        page.session.remove("analysis_result")
        
        print(f"解析結果を反映しました: {result}")

    def on_segment_change_internal(selected_index: int):
        """セグメント変更の内部処理"""
        nonlocal current_button
        
        if selected_index == 0:
            # 支出
            current_button = expense_button
        else:
            # 収入
            current_button = income_button
        
        # UIの更新（どちらも同じ構成）
        selected_control.controls = [
            price_field,
            date_field,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("カテゴリー"),
                        ft.Row(
                            current_button.button_list,
                            width=440,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                    ]
                ),
            ),
            ft.CupertinoFilledButton(
                content=ft.Text("　　　保存　　　"),
                opacity_on_click=0.3,
            ),
        ]
        page.update()

    def on_segment_change(event: ft.ControlEvent):
        try:
            selected_index = int(event.data) if event.data else 0
        except ValueError:
            selected_index = 0
        on_segment_change_internal(selected_index)

    # セグメントボタンにイベントハンドラを設定
    segment_button.on_change = on_segment_change

    # 初期表示の設定
    on_segment_change_internal(0)
    
    # セッションから解析結果を取得して適用
    apply_analysis_result()

    return ft.View(
        "/view1",
        [
            ft.AppBar(title=ft.Text("View 1"), leading=None),
            create_navigation_bar(page),
            ft.Column(
                [
                    ft.Container(
                        content=segment_button,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=12),
                    selected_control,
                ]
            ),
        ],
    )
