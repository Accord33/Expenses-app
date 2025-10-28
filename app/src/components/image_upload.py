"""画像アップロード機能"""
import flet as ft
import shutil
from datetime import datetime
from pathlib import Path


class ImageUploadHandler:
    """画像アップロード処理を管理するクラス"""
    
    def __init__(self, storage_pic_dir: Path, storage_temp_dir: Path):
        """
        Args:
            storage_pic_dir: 画像の最終保存先ディレクトリ
            storage_temp_dir: 一時アップロード先ディレクトリ
        """
        self.storage_pic_dir = storage_pic_dir
        self.storage_temp_dir = storage_temp_dir
        self.status_text = ft.Text()
        self.file_picker = None
    
    def on_upload_complete(self, event: ft.FilePickerUploadEvent) -> None:
        """
        アップロード完了後の処理
        
        Args:
            event: アップロード完了イベント
        """
        try:
            # アップロードされたファイルのパス（tempディレクトリ内）
            uploaded_file_name = event.file_name
            temp_file_path = self.storage_temp_dir / uploaded_file_name
            
            if not temp_file_path.exists():
                self.status_text.value = "✗ エラー: ファイルが見つかりません"
                self.status_text.update()
                return
            
            # タイムスタンプ付きのファイル名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = Path(uploaded_file_name).suffix
            new_filename = f"{timestamp}{file_extension}"
            
            # 最終保存先のパス
            destination_path = self.storage_pic_dir / new_filename
            
            # tempからpicにファイルを移動
            shutil.move(str(temp_file_path), str(destination_path))
            
            # 成功メッセージ
            self.status_text.value = f"✓ 保存完了: {new_filename}"
            print(f"画像を保存しました: {destination_path}")
            
        except Exception as ex:
            self.status_text.value = f"✗ エラー: {str(ex)}"
            print(f"画像の保存に失敗しました: {ex}")
        
        self.status_text.update()
    
    def pick_files_result(self, event: ft.FilePickerResultEvent, page: ft.Page) -> None:
        """
        ファイル選択後の処理
        
        Args:
            event: ファイル選択イベント
            page: Fletのページオブジェクト
        """
        if not event.files:
            self.status_text.value = "キャンセルされました"
            self.status_text.update()
            return
        
        try:
            # 選択されたファイル
            self.status_text.value = f"選択: {event.files[0].name}"
            self.status_text.update()
            
            # 一時アップロード先のURLを生成して各ファイルに設定
            upload_list = []
            for file_item in event.files:
                upload_url = page.get_upload_url(f"temp/{file_item.name}", 600)
                upload_list.append(
                    ft.FilePickerUploadFile(
                        file_item.name,
                        upload_url=upload_url,
                    )
                )
            
            # ファイルをアップロード
            self.file_picker.upload(upload_list)
            
            print(f"ファイルのアップロードを開始: {event.files[0].name}")
            
        except Exception as ex:
            self.status_text.value = f"✗ エラー: {str(ex)}"
            print(f"ファイルのアップロードに失敗しました: {ex}")
            self.status_text.update()
    
    def create_file_picker(self, page: ft.Page) -> ft.FilePicker:
        """
        FilePickerを作成して返す
        
        Args:
            page: Fletのページオブジェクト
            
        Returns:
            ft.FilePicker: 設定済みのFilePickerオブジェクト
        """
        self.file_picker = ft.FilePicker(
            on_result=lambda e: self.pick_files_result(e, page),
            on_upload=self.on_upload_complete
        )
        return self.file_picker
    
    def get_status_text(self) -> ft.Text:
        """
        ステータス表示用のTextコントロールを取得
        
        Returns:
            ft.Text: ステータス表示用テキスト
        """
        return self.status_text
