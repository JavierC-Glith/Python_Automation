import flet as ft

def main(page: ft.Page):
    # configuración básica de app
    page.title = "Automatización de Tareas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.colors.BLACK # Corregido: "c" minúscula
    page.theme_mode = ft.ThemeMode.DARK

    page.add(
        ft.Container(
            content=ft.Text(
                value="Automatización de Tareas",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_200 # Corregido: "c" minúscula
            ),
            # Corregido: Usamos las coordenadas matemáticas como te comenté antes
            alignment=ft.Alignment(0, 0), 
            expand=True
        )
    )

# Corregido: Volvemos a usar ft.app en lugar de ft.run
if __name__ == "__main__":
    ft.app(target=main)