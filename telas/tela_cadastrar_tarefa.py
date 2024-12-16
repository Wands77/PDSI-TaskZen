import flet as ft
from data.database import adicionar_tarefa
from datetime import datetime

def tela_cadastrar_tarefa(page: ft.Page, user_id: int):
    categorias = ["Pessoal", "Profissional", "Estudo"]

    def salvar_tarefa(e):
        titulo = titulo_input.value.strip()
        descricao = descricao_input.value.strip()
        prioridade = prioridade_dropdown.value
        categoria = categoria_dropdown.value

        if categoria == "Outra?":
            nova_categoria = nova_categoria_input.value.strip()
            if not nova_categoria:
                mensagem.value = "Digite uma nova categoria!"
                mensagem.color = "red"
                page.update()
                return
            categoria = nova_categoria
            if categoria not in categorias:
                categorias.append(categoria)  
                categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias + ["Outra?"]]
                categoria_dropdown.value = categoria
                nova_categoria_input.value = ""
                nova_categoria_input.visible = False

        if not (titulo and descricao and prioridade and categoria):
            mensagem.value = "Todos os campos são obrigatórios!"
            mensagem.color = "red"
            page.update()
            return

        try:
            data_vencimento = datetime(
                int(ano_dropdown.value),
                int(mes_dropdown.value),
                int(dia_dropdown.value),
                int(hora_dropdown.value),
                int(minuto_dropdown.value),
            )
            if data_vencimento <= datetime.now():
                mensagem.value = "A data e hora de vencimento devem ser futuras!"
                mensagem.color = "red"
                page.update()
                return
        except ValueError:
            mensagem.value = "Data ou horário inválido!"
            mensagem.color = "red"
            page.update()
            return

        adicionar_tarefa(user_id, titulo, descricao, data_vencimento.strftime("%d/%m/%Y %H:%M"), prioridade, categoria)
        mensagem.value = "Tarefa salva com sucesso!"
        mensagem.color = "green"
        page.update()

        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)  

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_inicial import main
        main(page, user_id)  

    def mostrar_nova_categoria(e):
        if categoria_dropdown.value == "Outra?":
            nova_categoria_input.visible = True
        else:
            nova_categoria_input.visible = False
        page.update()

    def abrir_seletor_data(e):
        page.dialog = data_dialog
        page.dialog.open = True
        page.update()

    def abrir_seletor_horario(e):
        page.dialog = horario_dialog
        page.dialog.open = True
        page.update()

    def fechar_seletor_data(e):
        page.dialog.open = False
        page.dialog = None
        page.update()

    def fechar_seletor_horario(e):
        page.dialog.open = False
        page.dialog = None
        page.update()

    def aplicar_selecao_data(e):
        data_selecionada = f"{dia_dropdown.value}/{mes_dropdown.value}/{ano_dropdown.value}"
        vencimento_data_button.text = f"Data: {data_selecionada}"
        fechar_seletor_data(e)

    def aplicar_selecao_horario(e):
        horario_selecionado = f"{hora_dropdown.value}:{minuto_dropdown.value}"
        vencimento_horario_button.text = f"Hora: {horario_selecionado}"
        fechar_seletor_horario(e)

    titulo_input = ft.TextField(label="Título:", width=320)
    descricao_input = ft.TextField(label="Descrição:", multiline=True, height=120, width=320)
    prioridade_dropdown = ft.Dropdown(
        label="Prioridade:", options=[ft.dropdown.Option(p) for p in ["Alta", "Média", "Baixa"]], width=320
    )
    categoria_dropdown = ft.Dropdown(
        label="Categoria:",
        options=[ft.dropdown.Option(c) for c in categorias + ["Outra?"]],
        width=320,
        on_change=mostrar_nova_categoria,  
    )
    nova_categoria_input = ft.TextField(label="Nova Categoria:", width=320, visible=False)
    mensagem = ft.Text(value="", size=14)

    vencimento_data_button = ft.ElevatedButton("Selecionar Data", on_click=abrir_seletor_data, width=150)
    vencimento_horario_button = ft.ElevatedButton("Selecionar Horário", on_click=abrir_seletor_horario, width=150)

    dias = [str(d) for d in range(1, 32)]
    meses = [str(m).zfill(2) for m in range(1, 13)]
    anos = [str(a) for a in range(datetime.now().year, datetime.now().year + 3)]
    horas = [str(h).zfill(2) for h in range(24)]
    minutos = [str(m).zfill(2) for m in range(0, 60)]

    dia_dropdown = ft.Dropdown(hint_text="Dia", options=[ft.dropdown.Option(d) for d in dias], width=70)
    mes_dropdown = ft.Dropdown(hint_text="Mês", options=[ft.dropdown.Option(m) for m in meses], width=70)
    ano_dropdown = ft.Dropdown(hint_text="Ano", options=[ft.dropdown.Option(a) for a in anos], width=70)

    hora_dropdown = ft.Dropdown(hint_text="Hora", options=[ft.dropdown.Option(h) for h in horas], width=70)
    minuto_dropdown = ft.Dropdown(hint_text="Minuto", options=[ft.dropdown.Option(m) for m in minutos], width=80)

    data_dialog = ft.AlertDialog(
        title=ft.Text("Selecionar Data", size=16, weight=ft.FontWeight.BOLD),
        content=ft.Row(
            [
                dia_dropdown,
                mes_dropdown,
                ano_dropdown,
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.ElevatedButton("Aplicar", on_click=aplicar_selecao_data, width=100),
            ft.ElevatedButton("Fechar", on_click=fechar_seletor_data, width=100),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    horario_dialog = ft.AlertDialog(
        title=ft.Text("Selecionar Horário", size=16, weight=ft.FontWeight.BOLD),
        content=ft.Row(
            [
                hora_dropdown,
                minuto_dropdown,
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.ElevatedButton("Aplicar", on_click=aplicar_selecao_horario, width=100),
            ft.ElevatedButton("Fechar", on_click=fechar_seletor_horario, width=100),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(
        ft.Column(
            [
                ft.Text("Nova Tarefa", size=20, weight=ft.FontWeight.BOLD, color="black"),
                titulo_input,
                descricao_input,
                ft.Row(
                    [vencimento_data_button, vencimento_horario_button],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                prioridade_dropdown,
                categoria_dropdown,
                nova_categoria_input,
                mensagem,
                ft.Row(
                    [
                        ft.ElevatedButton("Voltar", on_click=voltar_tela_inicial, width=150, height=45),
                        ft.ElevatedButton("Salvar", on_click=salvar_tarefa, width=150, height=45),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )
