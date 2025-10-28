"""アプリケーション設定管理"""
import os
from pathlib import Path
import dotenv

dotenv.load_dotenv()


class AppConfig:
    """アプリケーション設定クラス"""
    
    @staticmethod
    def get_secret_key() -> str:
        """
        Fletのアップロード機能用シークレットキーを取得
        
        Returns:
            str: シークレットキー（環境変数 or デフォルト値）
        """
        return os.getenv("FLET_SECRET_KEY", "dev-secret-key-12345")
    
    @staticmethod
    def get_storage_dir() -> Path:
        """
        ストレージディレクトリの絶対パスを取得
        
        Returns:
            Path: storageディレクトリの絶対パス
        """
        current_dir = Path(__file__).parent.parent  # /app/
        return current_dir / "storage"
    
    @staticmethod
    def setup_environment() -> None:
        """
        環境変数をセットアップ
        FLET_SECRET_KEYが設定されていない場合はデフォルト値を設定
        """
        if not os.getenv("FLET_SECRET_KEY"):
            os.environ["FLET_SECRET_KEY"] = AppConfig.get_secret_key()
