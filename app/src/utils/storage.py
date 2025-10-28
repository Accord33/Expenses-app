"""ストレージディレクトリ管理ユーティリティ"""
from pathlib import Path
from typing import Dict


class StoragePathManager:
    """ストレージディレクトリのパス管理クラス"""
    
    @staticmethod
    def get_storage_paths(base_file: Path) -> Dict[str, Path]:
        """
        storageディレクトリ配下の各パスを取得
        
        Args:
            base_file: 基準となるファイルのパス（通常は __file__）
            
        Returns:
            Dict[str, Path]: ストレージパスの辞書
                - 'pic': 画像保存ディレクトリ
                - 'temp': 一時ファイルディレクトリ
                - 'data': データ保存ディレクトリ
        """
        # view1.py → views/ → src/ → app/ → storage/
        storage_base = base_file.parent.parent.parent / "storage"
        
        return {
            'pic': storage_base / "pic",
            'temp': storage_base / "temp",
            'data': storage_base / "data"
        }
    
    @staticmethod
    def ensure_directories(paths: Dict[str, Path]) -> None:
        """
        ディレクトリが存在することを確認し、なければ作成
        
        Args:
            paths: 確認するパスの辞書
        """
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
