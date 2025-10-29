import flet as ft
from components.navigation import create_navigation_bar
from components.image_upload import ImageUploadHandler
from utils.storage import StoragePathManager
from pathlib import Path


def create_view4(page: ft.Page):
    """スクショ読み込み専用画面"""
    
    # ストレージパスの取得と初期化
    storage_paths = StoragePathManager.get_storage_paths(Path(__file__))
    StoragePathManager.ensure_directories(storage_paths)
    
    # 解析結果を表示するコンテナ
    analysis_result_container = ft.Container(
        visible=False,
        padding=20,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=10,
    )
    
    # 画像プレビュー用のコンテナ
    image_preview = ft.Container(
        visible=False,
        alignment=ft.alignment.center,
    )
    
    # 入力画面に反映ボタン
    apply_button = ft.CupertinoFilledButton(
        content=ft.Text("入力画面に反映"),
        opacity_on_click=0.3,
        visible=False,
        on_click=lambda e: apply_to_input_view(),
    )
    
    # 解析結果を保持する変数
    current_analysis_result = {}
    
    def apply_to_input_view():
        """解析結果を入力画面に反映して遷移"""
        if current_analysis_result:
            # ページセッションに解析結果を保存
            page.session.set("analysis_result", current_analysis_result)
            # View1に遷移
            page.go("/view1")
    
    def on_analysis_complete(result: dict, image_path: Path):
        """
        Gemini解析完了時に呼ばれる関数
        
        Args:
            result: 解析結果 {"price": str, "date": str, "category": str, "type": str} or {"error": str}
            image_path: 解析した画像のパス
        """
        nonlocal current_analysis_result
        
        if "error" in result:
            # エラー表示
            analysis_result_container.content = ft.Column([
                ft.Text("❌ 解析エラー", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                ft.Text(result["error"], color=ft.Colors.RED),
            ])
            analysis_result_container.visible = True
            apply_button.visible = False
            current_analysis_result = {}
        else:
            # 解析結果を保存
            current_analysis_result = result
            
            # 結果表示を更新
            result_type = result.get("type", "expense")
            type_text = "収入" if result_type == "income" else "支出"
            type_color = ft.Colors.GREEN if result_type == "income" else ft.Colors.RED
            
            analysis_result_container.content = ft.Column([
                ft.Text("✅ 解析完了", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                ft.Divider(height=10),
                ft.Row([
                    ft.Text("種類:", weight=ft.FontWeight.BOLD),
                    ft.Text(type_text, color=type_color, weight=ft.FontWeight.BOLD),
                ]),
                ft.Row([
                    ft.Text("金額:", weight=ft.FontWeight.BOLD),
                    ft.Text(f"{result.get('price', '')}円"),
                ]),
                ft.Row([
                    ft.Text("日付:", weight=ft.FontWeight.BOLD),
                    ft.Text(result.get('date', '')),
                ]),
                ft.Row([
                    ft.Text("カテゴリ:", weight=ft.FontWeight.BOLD),
                    ft.Text(result.get('category', '')),
                ]),
            ])
            analysis_result_container.visible = True
            apply_button.visible = True
        
        # 画像プレビューを表示
        try:
            image_preview.content = ft.Image(
                src=str(image_path),
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
                border_radius=10,
            )
            image_preview.visible = True
        except Exception as e:
            print(f"画像プレビューエラー: {e}")
        
        page.update()
    
    # 画像アップロードハンドラーの初期化
    upload_handler = ImageUploadHandler(
        storage_pic_dir=storage_paths["pic"],
        storage_temp_dir=storage_paths["temp"],
        on_analysis_complete=on_analysis_complete,
    )
    
    # FilePickerの作成
    pick_files_dialog = upload_handler.create_file_picker(page)
    status_text = upload_handler.get_status_text()
    
    page.overlay.append(pick_files_dialog)
    
    return ft.View(
        "/view4",
        [
            ft.AppBar(
                title=ft.Text("レシート読み込み"),
                leading=None,
            ),
            create_navigation_bar(page),
            ft.Column(
                [
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(
                                    ft.Icons.CAMERA_ALT,
                                    size=60,
                                    color=ft.Colors.BLUE_400,
                                ),
                                ft.Container(height=10),
                                ft.CupertinoFilledButton(
                                    content=ft.Text("📷 スクショを選択"),
                                    opacity_on_click=0.3,
                                    on_click=lambda e: pick_files_dialog.pick_files(),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(height=10),
                    status_text,
                    ft.Container(height=20),
                    image_preview,
                    ft.Container(height=20),
                    analysis_result_container,
                    ft.Container(height=20),
                    ft.Container(
                        content=apply_button,
                        alignment=ft.alignment.center,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
        ],
    )
