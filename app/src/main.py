import flet as ft
from views import create_view1, create_view2, create_view3, create_category_detail
import urllib.parse
import dotenv
import os
from pathlib import Path

dotenv.load_dotenv()

# アップロード機能のためのsecret_keyを環境変数に設定
if not os.getenv("FLET_SECRET_KEY"):
    os.environ["FLET_SECRET_KEY"] = "dev-secret-key-12345"

# プロジェクトのstorageディレクトリへの絶対パスを取得
current_dir = Path(__file__).parent.parent  # /app/
storage_dir = current_dir / "storage"



def main(page: ft.Page):

    def route_change(handler):
        if handler.route == "/view1":
            page.views.clear()
            page.views.append(create_view1(page))
        elif handler.route == "/view2":
            page.views.clear()
            page.views.append(create_view2(page))
        elif handler.route == "/view3":
            page.views.clear()
            page.views.append(create_view3(page))
        elif handler.route.startswith("/category_detail"):
            parsed_url = urllib.parse.urlparse(handler.route)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            category = query_params.get("category", [""])[0]
            page.views.append(create_view2(page))
            page.views.append(create_category_detail(page, category))
        page.update()


    page.on_route_change = route_change
    page.go("/view1")


ft.app(
    target=main,
    upload_dir=str(storage_dir)
)