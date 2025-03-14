import flet as ft
import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """تحميل المهام من ملف JSON"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    """حفظ المهام إلى ملف JSON"""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def main(page: ft.Page):
    page.title = "قائمة المهام"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_200
    page.scroll = ft.ScrollMode.AUTO

    tasks = load_tasks()

    title = ft.Text(
        "📌 قائمة المهام", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE
    )

    task_input = ft.TextField(
        hint_text="أضف مهمة جديدة...",
        expand=True,
        autofocus=True,
        border_radius=10,
        border_color=ft.colors.BLUE,
    )

    task_list = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    def update_task_list():
        """تحديث عرض المهام"""
        task_list.controls.clear()
        for task in tasks:
            index = tasks.index(task)
            checkbox = ft.Checkbox(
                label=task["title"],
                value=task["done"],
                on_change=lambda e, i=index: toggle_task(i),
            )
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED,
                on_click=lambda e, i=index: delete_task(i),
            )

            row = ft.Row([checkbox, delete_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            task_list.controls.append(row)
        page.update()

    def add_task(e):
        """إضافة مهمة جديدة"""
        if task_input.value.strip():
            tasks.append({"title": task_input.value.strip(), "done": False})
            save_tasks(tasks)
            task_input.value = ""
            update_task_list()

    def toggle_task(index):
        """تحديث حالة المهمة"""
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
        update_task_list()

    def delete_task(index):
        """حذف المهمة"""
        del tasks[index]
        save_tasks(tasks)
        update_task_list()

    update_task_list()

    add_button = ft.ElevatedButton("➕ إضافة", bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, on_click=add_task)

    input_row = ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.CENTER)

    page.add(ft.Container(title, padding=20), input_row, task_list)


ft.app(target=main)
