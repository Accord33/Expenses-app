import flet as ft
from components.navigation import create_navigation_bar
from components.image_upload import ImageUploadHandler
from utils.storage import StoragePathManager
from pathlib import Path


class ContentButton:
    def __init__(self, page: ft.Page):
        self.page = page
        self.button_list = []
        self.name_list = ["食費", "交通費", "娯楽費", "日用品"]
        self.focus_index = 0

        for i, name in enumerate(self.name_list):
            self.button_list.append(
                ft.Container(
                    content=ft.CupertinoButton(
                        content=ft.Text(
                            f"{name}",
                            color=ft.CupertinoColors.BLACK,
                        ),
                        opacity_on_click=0.3,
                        on_click=lambda e, idx=i: self.focus_button(idx),
                    ),
                    border=ft.border.all(1, ft.Colors.BLACK),
                    border_radius=10,
                )
            )

        self.focus_button(self.focus_index)

    def focus_button(self, index: int):
        self.button_list[self.focus_index].border = ft.border.all(1, ft.Colors.WHITE)
        self.focus_index = index
        self.button_list[index].border = ft.border.all(1, ft.Colors.BLUE)
        self.page.update()

    def get_focused_content(self):
        return self.name_list[self.focus_index]


def create_view1(page: ft.Page):
    selected_control = ft.Column()
    
    # ストレージパスの取得と初期化
    storage_paths = StoragePathManager.get_storage_paths(Path(__file__))
    StoragePathManager.ensure_directories(storage_paths)
    
    # 入力フィールドの参照を保持
    price_field = ft.TextField(
        adaptive=True,
        label="金額",
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
    )
    date_field = ft.TextField(
        adaptive=True,
        label="日付：YYYYMMDD",
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
    )
    
    content_button = ContentButton(page)
    
    # Gemini解析完了時のコールバック関数
    def on_analysis_complete(result: dict, image_path: Path):
        """
        Gemini解析完了時に呼ばれる関数
        
        Args:
            result: 解析結果 {"price": str, "date": str, "category": str} or {"error": str}
            image_path: 解析した画像のパス
        """
        if "error" in result:
            print(f"解析エラー: {result['error']}")
            return
        
        # フィールドに値を設定
        price_field.value = result.get("price", "")
        date_field.value = result.get("date", "")
        
        # カテゴリを設定
        category = result.get("category", "")
        category_map = {
            "食費": 0,
            "交通費": 1,
            "娯楽費": 2,
            "日用品": 3
        }
        if category in category_map:
            content_button.focus_button(category_map[category])
        
        # 画面を更新
        page.update()
        print(f"解析結果を反映しました: {result}")
    
    # 画像アップロードハンドラーの初期化（コールバックを渡す）
    upload_handler = ImageUploadHandler(
        storage_pic_dir=storage_paths['pic'],
        storage_temp_dir=storage_paths['temp'],
        on_analysis_complete=on_analysis_complete
    )
    
    # FilePickerの作成
    pick_files_dialog = upload_handler.create_file_picker(page)
    status_text = upload_handler.get_status_text()

    page.overlay.append(pick_files_dialog)

    def on_segment_change(event: ft.ControlEvent):
        try:
            selected_index = int(event.data) if event.data else 0
        except Exception:
            selected_index = 0
        if selected_index == 0:
            selected_control.controls = [
                price_field,
                date_field,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("カテゴリー"),
                            ft.Row(
                                content_button.button_list,
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
                ft.CupertinoFilledButton(
                    content=ft.Text("スクショから取り込み"),
                    opacity_on_click=0.3,
                    on_click=lambda e: pick_files_dialog.pick_files(),
                ),
                status_text,
            ]
        else:
            selected_control.controls = [ft.Text("収入")]
        page.update()

    # 初期表示の設定（ダミーイベントを作成）
    class DummyEvent:
        data = "0"
    on_segment_change(DummyEvent())

    return ft.View(
        "/view1",
        [
            ft.AppBar(title=ft.Text("View 1"),leading=None),
            create_navigation_bar(page),
            ft.Column(
                [
                    ft.Container(
                        content=ft.CupertinoSlidingSegmentedButton(
                            selected_index=0,
                            thumb_color=ft.Colors.BLUE_400,
                            on_change=on_segment_change,
                            controls=[
                                ft.Text("　　支出　　"),
                                ft.Text("　　収入　　"),
                            ],
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=12),
                    selected_control,
                ]
            ),
        ],
    )
