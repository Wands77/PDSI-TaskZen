import flet as ft
from telas.tela_cadastrar_tarefa import tela_cadastrar_tarefa
from telas.tela_lista_tarefas import tela_lista_tarefas
from data.sessao import limpar_sessao


def main(page: ft.Page, user_id: int):  # Recebe o ID do usuário como parâmetro
    page.title = "TaskZen"
    page.theme_mode = "light"
    page.bgcolor = "#f0f0f0"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 360
    page.window_height = 640
    page.window_resizable = False

    # Variável de controle para o estado do diálogo
    dialog_aberto = False

    # Função para abrir a tela de cadastro de tarefas
    def abrir_cadastrar_tarefa(e):
        page.clean()
        tela_cadastrar_tarefa(page, user_id)

    # Função para abrir a tela de listagem de tarefas
    def abrir_listar_tarefas(e):
        page.clean()
        tela_lista_tarefas(page, user_id)
        
    def sair_confirmado(e):
        nonlocal dialog_aberto
        limpar_sessao()  # Remove o usuário da sessão
        dialog.open = False
        dialog_aberto = False
        page.update()
        page.clean()
        from telas.login import tela_login
        tela_login(page)


    # Função para abrir o dialog de confirmação
    def confirmar_sair(e):
        nonlocal dialog_aberto
        if not dialog_aberto:  # Garante que o diálogo só abre se não estiver visível
            dialog_aberto = True
            dialog.open = True
            page.update()

    # Função para cancelar a saída
    def cancelar_sair(e):
        nonlocal dialog_aberto
        dialog.open = False
        dialog_aberto = False  # Atualiza o estado do diálogo
        page.update()

    # Cabeçalho
    header = ft.Row(
        [
            ft.Image(src=r"C:\Users\wands\OneDrive\Documentos\taskzen\logo\icon.png", width=50, height=50, fit=ft.ImageFit.CONTAIN),
            ft.Text("TaskZen", size=24, weight=ft.FontWeight.BOLD, color="black"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Pop-up de confirmação de saída
    dialog = ft.AlertDialog(
        title=ft.Text("Sair do TaskZen"),
        content=ft.Text("Tem certeza que deseja sair da conta?"),
        actions=[
            ft.ElevatedButton(
                "Sim",
                on_click=sair_confirmado,
                bgcolor=ft.colors.RED,
                color=ft.colors.WHITE,
            ),
            ft.TextButton("Cancelar", on_click=cancelar_sair),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dialog  # Associa o dialog à página

    # Layout principal
    page.add(
        ft.Column(
            [
                header,
                ft.ElevatedButton("Criar Tarefa", width=320, height=50, on_click=abrir_cadastrar_tarefa),
                ft.ElevatedButton("Ver Tarefas", width=320, height=50, on_click=abrir_listar_tarefas),
                ft.ElevatedButton(
                    "Sair",
                    width=320,
                    height=50,
                    on_click=confirmar_sair,
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )
