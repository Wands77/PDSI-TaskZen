import flet as ft
from data.database import adicionar_usuario, email_existe, validar_email


def tela_cadastro(page: ft.Page):
    def validar_criterios_senha(senha):
        criterios = {
            "tamanho": len(senha) >= 8,
            "maiuscula": any(c.isupper() for c in senha),
            "minuscula": any(c.islower() for c in senha),
            "numero": any(c.isdigit() for c in senha),
        }

        criterio_tamanho.color = "green" if criterios["tamanho"] else "red"
        criterio_maiuscula.color = "green" if criterios["maiuscula"] else "red"
        criterio_minuscula.color = "green" if criterios["minuscula"] else "red"
        criterio_numero.color = "green" if criterios["numero"] else "red"

        page.update()
        return all(criterios.values())

    def realizar_cadastro(e):
        nome = nome_input.value
        email = email_input.value
        senha = senha_input.value

        if not nome or not email or not senha:
            msg_feedback.value = "Preencha todos os campos!"
            msg_feedback.color = "red"
        elif not validar_email(email):
            msg_feedback.value = "Formato de e-mail inválido!"
            msg_feedback.color = "red"
        elif email_existe(email):
            msg_feedback.value = "E-mail já cadastrado!"
            msg_feedback.color = "red"
        elif not validar_criterios_senha(senha):
            msg_feedback.value = "Senha inválida! Verifique os critérios em vermelho."
            msg_feedback.color = "red"
        else:
            adicionar_usuario(nome, email, senha)
            exibir_popup_sucesso()
        page.update()

    def exibir_popup_sucesso():
        dialog = ft.AlertDialog(
            title=ft.Text("Cadastro Concluído!"),
            content=ft.Text("Seu cadastro foi realizado com sucesso."),
            actions=[ft.ElevatedButton("OK", on_click=voltar_login)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def voltar_login(e=None):
        page.clean()
        from telas.login import tela_login
        tela_login(page)

    nome_input = ft.TextField(label="Nome Completo", width=300)
    email_input = ft.TextField(label="Email", width=300)
    senha_input = ft.TextField(
        label="Senha",
        width=300,
        password=True,
        can_reveal_password=True,
        on_change=lambda e: validar_criterios_senha(e.control.value),
    )
    btn_cadastrar = ft.ElevatedButton("Cadastrar", on_click=realizar_cadastro, width=300, height=45)
    btn_voltar = ft.TextButton("Voltar para Login", on_click=voltar_login, width=300)
    msg_feedback = ft.Text("", size=14)

    criterio_tamanho = ft.Text("- Pelo menos 8 caracteres", size=14, color="red")
    criterio_maiuscula = ft.Text("- Pelo menos uma letra maiúscula", size=14, color="red")
    criterio_minuscula = ft.Text("- Pelo menos uma letra minúscula", size=14, color="red")
    criterio_numero = ft.Text("- Pelo menos um número", size=14, color="red")

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Cadastro no TaskZen",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                nome_input,
                email_input,
                senha_input,
                ft.Text("A senha deve atender aos critérios:", size=14, weight=ft.FontWeight.BOLD),
                criterio_tamanho,
                criterio_maiuscula,
                criterio_minuscula,
                criterio_numero,
                ft.Row(
                    [
                        btn_cadastrar,  
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10, 
                ),
                ft.Row(
                    [
                        btn_voltar,  
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10, 
                ),
                msg_feedback,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,  
            expand=True,
        )
    )
