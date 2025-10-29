import flet as ft
from views import create_view1, create_view2, create_view3, create_view4, create_category_detail
from config import AppConfig
import urllib.parse

# 環境変数の初期化
AppConfig.setup_environment()


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
        elif handler.route == "/view4":
            page.views.clear()
            page.views.append(create_view4(page))
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
    upload_dir=str(AppConfig.get_storage_dir())
)