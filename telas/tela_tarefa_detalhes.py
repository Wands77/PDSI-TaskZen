import flet as ft
from data.database import excluir_tarefa, atualizar_tarefa
from datetime import datetime

def tela_tarefa_detalhes(page: ft.Page, tarefa, usuario_id: int):
    tarefa_id, titulo, descricao, prazo, prioridade, categoria, _ = tarefa

    def excluir(e):
        excluir_tarefa(tarefa_id)
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

    def salvar(e):
        categoria_final = categoria_dropdown.value
        if categoria_final == "Outra?":
            categoria_final = nova_categoria_input.value.strip()
            if not categoria_final:
                mensagem.value = "Digite uma nova categoria!"
                mensagem.color = "red"
                page.update()
                return
            if categoria_final not in categorias:
                categorias.append(categoria_final)
                categoria_dropdown.options = [ft.dropdown.Option(c) for c in categorias + ["Outra?"]]
                categoria_dropdown.value = categoria_final

        try:
            data_vencimento = datetime(
                int(ano_dropdown.value),
                int(mes_dropdown.value),
                int(dia_dropdown.value),
                int(hora_dropdown.value),
                int(minuto_dropdown.value),
            )
        except ValueError:
            mensagem.value = "Data ou horário inválido!"
            mensagem.color = "red"
            page.update()
            return

        atualizar_tarefa(
            tarefa_id,
            titulo_input.value,
            descricao_input.value,
            data_vencimento.strftime("%d/%m/%Y %H:%M"),
            prioridade_dropdown.value,
            categoria_final,
        )
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

    def voltar_tela_inicial(e):
        page.clean()
        from telas.tela_lista_tarefas import tela_lista_tarefas
        tela_lista_tarefas(page, usuario_id)

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
        data_button.text = f"Data: {data_selecionada}"
        fechar_seletor_data(e)

    def aplicar_selecao_horario(e):
        horario_selecionado = f"{hora_dropdown.value}:{minuto_dropdown.value}"
        horario_button.text = f"Hora: {horario_selecionado}"
        fechar_seletor_horario(e)

    categorias = ["Pessoal", "Profissional", "Estudo"]
    if categoria not in categorias:
        categorias.append(categoria)

    prioridades = ["Alta", "Média", "Baixa"]

    now = datetime.strptime(prazo, "%d/%m/%Y %H:%M")
    dias = [str(d) for d in range(1, 32)]
    meses = [str(m).zfill(2) for m in range(1, 13)]
    anos = [str(a) for a in range(datetime.now().year, datetime.now().year + 3)]  
    horas = [str(h).zfill(2) for h in range(24)]
    minutos = [str(m).zfill(2) for m in range(0, 60)]  

    dia_dropdown = ft.Dropdown(hint_text="Dia", options=[ft.dropdown.Option(d) for d in dias], value=str(now.day), width=70)
    mes_dropdown = ft.Dropdown(hint_text="Mês", options=[ft.dropdown.Option(m) for m in meses], value=str(now.month).zfill(2), width=70)
    ano_dropdown = ft.Dropdown(hint_text="Ano", options=[ft.dropdown.Option(a) for a in anos], value=str(now.year), width=70)
    hora_dropdown = ft.Dropdown(hint_text="Hora", options=[ft.dropdown.Option(h) for h in horas], value=str(now.hour).zfill(2), width=70)
    minuto_dropdown = ft.Dropdown(hint_text="Minuto", options=[ft.dropdown.Option(m) for m in minutos], value=str(now.minute).zfill(2), width=70)

    titulo_input = ft.TextField(value=titulo, label="Título:", width=320)
    descricao_input = ft.TextField(value=descricao, label="Descrição:", multiline=True, height=120, width=320)
    prioridade_dropdown = ft.Dropdown(
        value=prioridade,
        options=[ft.dropdown.Option(p) for p in prioridades],
        label="Prioridade",
        width=320,
    )
    categoria_dropdown = ft.Dropdown(
        value=categoria,
        options=[ft.dropdown.Option(c) for c in categorias + ["Outra?"]],
        label="Categoria",
        width=320,
        on_change=mostrar_nova_categoria,
    )
    nova_categoria_input = ft.TextField(label="Nova Categoria:", width=320, visible=False)
    mensagem = ft.Text(value="", size=14)

    data_button = ft.ElevatedButton("Editar Data", on_click=abrir_seletor_data, width=150)
    horario_button = ft.ElevatedButton("Editar Horário", on_click=abrir_seletor_horario, width=150)

    data_dialog = ft.AlertDialog(
        title=ft.Text("Editar Data", size=16, weight=ft.FontWeight.BOLD),
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
        title=ft.Text("Editar Horário", size=16, weight=ft.FontWeight.BOLD),
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
                ft.Text("Editar Tarefa", size=20, weight=ft.FontWeight.BOLD, color="black"),
                titulo_input,
                descricao_input,
                ft.Row(
                    [data_button, horario_button],
                    spacing=10,
                ),
                prioridade_dropdown,
                categoria_dropdown,
                nova_categoria_input,
                mensagem,
                ft.Row(
                    [
                        ft.ElevatedButton("Voltar", on_click=voltar_tela_inicial, expand=1, height=45),
                        ft.ElevatedButton("Excluir", on_click=excluir, expand=1, height=45),
                        ft.ElevatedButton("Salvar", on_click=salvar, expand=1, height=45),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )
