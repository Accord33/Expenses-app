import flet as ft
from components.navigation import create_navigation_bar


class ContentButton:
    def __init__(self, page: ft.Page):
        self.page = page
        self.button_list = []
        name_list = ["食費", "交通費", "娯楽費", "日用品"]
        self.focus_index = 0

        for i, name in enumerate(name_list):
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

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        upload_url = page.get_upload_url(f"uploads/{e.files[0].name}", 60)
        e.files[0].upload_url = upload_url
        print("upload_url:", upload_url)
        pick_files_dialog.upload(e.files[0])
        print("Uploaded file to:", upload_url)
        selected_files.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
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
