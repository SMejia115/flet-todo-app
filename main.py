import flet as ft
import json
from pathlib import Path

# Ruta para guardar las tareas
TASKS_FILE = Path("tasks.json")

# Función para cargar tareas desde el archivo
def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Función para guardar tareas en el archivo
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def main(page: ft.Page):
    page.title = "To-Do App"
    page.theme_mode = "LIGHT"
    tasks = load_tasks()

    # Función para actualizar la lista visualmente
    def update_task_list():
      task_list.controls.clear()
      for idx, task in enumerate(tasks):
          task_text = task["text"]
          is_completed = task["completed"]

          # Tarea con botón para eliminar y opción de marcar completada
          task_row = ft.Row(
              controls=[
                  ft.Checkbox(
                      value=is_completed,
                      on_change=lambda e, idx=idx: toggle_complete(idx, e.control.value),
                  ),
                  ft.Text(
                      task_text,
                      style=ft.TextStyle(decoration="line-through" if is_completed else None),
                      color="green" if is_completed else "black",
                  ),
                  ft.IconButton(
                      icon=ft.icons.DELETE,
                      on_click=lambda e, idx=idx: delete_task(idx),
                  ),
              ]
          )
          task_list.controls.append(task_row)
      page.update()

    # Función para añadir una nueva tarea
    def add_task(e):
        task_text = task_input.value.strip()
        if task_text:
            tasks.append({"text": task_text, "completed": False})
            task_input.value = ""
            save_tasks(tasks)
            update_task_list()

    # Función para eliminar una tarea
    def delete_task(idx):
        del tasks[idx]
        save_tasks(tasks)
        update_task_list()

    # Función para marcar una tarea como completada
    def toggle_complete(idx, value):
        tasks[idx]["completed"] = value
        save_tasks(tasks)
        update_task_list()

    # Entrada para nuevas tareas
    task_input = ft.TextField(label="Nueva Tarea", on_submit=add_task)

    # Botón para añadir tareas
    add_button = ft.ElevatedButton(text="Añadir", on_click=add_task)

    # Lista de tareas
    task_list = ft.Column()

    # Inicializa la lista visual
    update_task_list()

    # Layout principal
    page.add(
        ft.Column(
            controls=[
                ft.Text("To-Do App Mejorada", size=30, weight="bold"),
                task_input,
                add_button,
                ft.Divider(),
                ft.Text("Tareas:", size=20),
                task_list,
            ]
        )
    )

# Ejecuta la aplicación
if __name__ == "__main__":
    ft.app(target=main)
