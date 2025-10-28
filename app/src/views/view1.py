import flet as ft
from components.navigation import create_navigation_bar
import shutil
from datetime import datetime
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
    
    # 画像保存先ディレクトリのパスを取得（プロジェクトルートからの相対パス）
    current_file = Path(__file__)
    storage_pic_dir = current_file.parent.parent.parent / "storage" / "pic"
    storage_temp_dir = current_file.parent.parent.parent / "storage" / "temp"
    
    # ディレクトリが存在しない場合は作成
    storage_pic_dir.mkdir(parents=True, exist_ok=True)
    storage_temp_dir.mkdir(parents=True, exist_ok=True)

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        """アップロード進行状況の表示"""
        selected_files.value = f"アップロード中... {e.progress * 100:.0f}%" if e.progress else "アップロード中..."
        selected_files.update()

    def on_upload_complete(e: ft.FilePickerUploadEvent):
        """アップロード完了後の処理"""
        try:
            # アップロードされたファイルのパス（tempディレクトリ内）
            uploaded_file_name = e.file_name
            temp_file_path = storage_temp_dir / uploaded_file_name
            
            if not temp_file_path.exists():
                selected_files.value = f"✗ エラー: ファイルが見つかりません"
                selected_files.update()
                return
            
            # タイムスタンプ付きのファイル名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = Path(uploaded_file_name).suffix
            new_filename = f"{timestamp}{file_extension}"
            
            # 最終保存先のパス
            destination_path = storage_pic_dir / new_filename
            
            # tempからpicにファイルを移動
            shutil.move(str(temp_file_path), str(destination_path))
            
            # 成功メッセージ
            selected_files.value = f"✓ 保存完了: {new_filename}"
            print(f"画像を保存しました: {destination_path}")
            
        except Exception as ex:
            selected_files.value = f"✗ エラー: {str(ex)}"
            print(f"画像の保存に失敗しました: {ex}")
        
        selected_files.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        """ファイル選択後の処理"""
        if not e.files:
            selected_files.value = "キャンセルされました"
            selected_files.update()
            return
        
        try:
            # 選択されたファイル
            selected_files.value = f"選択: {e.files[0].name}"
            selected_files.update()
            
            # 一時アップロード先のURLを生成して各ファイルに設定
            upload_list = []
            for f in e.files:
                upload_url = page.get_upload_url(f"temp/{f.name}", 600)
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=upload_url,
                    )
                )
            
            # ファイルをアップロード
            pick_files_dialog.upload(upload_list)
            
            print(f"ファイルのアップロードを開始: {e.files[0].name}")
            
        except Exception as ex:
            selected_files.value = f"✗ エラー: {str(ex)}"
            print(f"ファイルのアップロードに失敗しました: {ex}")
            selected_files.update()

    pick_files_dialog = ft.FilePicker(
        on_result=pick_files_result,
        on_upload=on_upload_complete
    )
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)
    content_button = ContentButton(page)

    def on_segment_change(e: ft.ControlEvent):
        try:
            idx = int(e.data)
        except Exception:
            idx = 0
        if idx == 0:
            selected_control.controls = [
                ft.TextField(
                    adaptive=True,
                    label="金額",
                    label_style=ft.TextStyle(color=ft.Colors.GREY_400),
                ),
                ft.TextField(
                    adaptive=True,
                    label="日付：YYYYMMDD",
                    label_style=ft.TextStyle(color=ft.Colors.GREY_400),
                ),
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
                selected_files,
            ]
        else:
            selected_control.controls = [ft.Text("収入")]
        page.update()

    on_segment_change(None)  # 初期表示の設定

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
