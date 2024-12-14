import flet as ft
from data.sessao import salvar_sessao
from data.database import validar_login, validar_email


def tela_login(page: ft.Page):
    page.title = "TaskZen - Login"
    page.theme_mode = "light"
    page.bgcolor = "#d9d9d9"  
    page.window_width = 360
    page.window_height = 640
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def realizar_login(e):
        email = email_input.value
        senha = senha_input.value

        if email and senha:
            if not validar_email(email):
                msg_feedback.value = "Formato de e-mail inválido!"
                msg_feedback.color = "red"
            else:
                user_id = validar_login(email, senha)
                if user_id:
                    salvar_sessao(user_id) 
                    from telas.tela_inicial import main
                    page.clean()
                    main(page, user_id=user_id)
                else:
                    msg_feedback.value = "Email ou senha inválidos."
                    msg_feedback.color = "red"
        else:
            msg_feedback.value = "Por favor, preencha todos os campos."
            msg_feedback.color = "red"
        page.update()

    def redirecionar_cadastro(e):
        page.clean()
        from telas.tela_cadastro import tela_cadastro
        tela_cadastro(page)

    logo = ft.Image(
        src=r"C:\Users\wands\OneDrive\Documentos\taskzen\logo\icon.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )

    email_input = ft.TextField(label="Email", width=300)
    senha_input = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)
    btn_login = ft.ElevatedButton("Entrar", on_click=realizar_login, width=300)
    msg_feedback = ft.Text("", size=14)
    btn_cadastrar = ft.TextButton("Cadastrar", on_click=redirecionar_cadastro, width=300)

    page.add(
        ft.Column(
            [
                logo,
                ft.Text(
                    "TaskZen",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK87,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                email_input,
                senha_input,
                btn_login,
                msg_feedback,
                btn_cadastrar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )
